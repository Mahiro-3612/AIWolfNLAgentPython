from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from utils import agent_util

if TYPE_CHECKING:
    import configparser

    from aiwolf_nlp_common.protocol.info import Info
    from aiwolf_nlp_common.protocol.list.talk_list import TalkList
    from aiwolf_nlp_common.protocol.list.whisper_list import WhisperList
    from aiwolf_nlp_common.protocol.setting import Setting
    from aiwolf_nlp_common.role import Role

    from utils.agent_log import AgentLog

import random
from threading import Thread
from typing import Callable

from aiwolf_nlp_common import Action
from aiwolf_nlp_common.protocol import Packet
from aiwolf_nlp_common.role import RoleInfo

import concurrent.futures
from player.agent import Agent
from player_openai.stance import Stance
from player_openai.colour_scale import Colour_Scale
from player_openai.coming_out import Coming_Out
from player_openai.my_tactics import MyTactics

from player_openai.functions.generate_statement import generate_statement

from player_openai.dev_functions.log import clear_log, log, log_talk

import sys


class Agent_OpenAI(Agent):
    timeout = Agent.timeout

    def __init__(
        self,
        config: configparser.ConfigParser | None = None,
        name: str | None = None,
        agent_log: AgentLog | None = None,
    ) -> None:

        super().__init__(config, name, agent_log)

        # ゲーム状況
        self.day: int = 0

        # 考察Class
        self.my_tactics = None
        self.stances: list[Stance] = []
        self.colour_scales: list[Colour_Scale] = []
        self.coming_outs: list[Coming_Out] = []

    def initialize(self) -> None:
        super().initialize()
        self.init_stances()
        self.init_colour_scales()
        self.init_coming_outs()
        self.init_tactics()

        clear_log(self.index)

    def _get_agent_status(self, agent_num: int) -> bool | None:
        """
        エージェントの生存状態を取得
        Args:
            agent_num (int): エージェント番号（0から始まる）
        Returns:
            bool: 生存していればTrue、死亡していればFalse
        """
        agent_id = f"Agent[{agent_num + 1:02d}]"

        if self.info is None:
            return None

        alive_agents = self.info.status_map.get_alive_agent_list()

        self.alive_agents_num = len(alive_agents)

        if agent_id in alive_agents:
            return True

        else:
            return False

    def daily_initialize(self) -> None:
        super().daily_initialize()

        self.alive = []
        # スタンス情報の更新
        for agent_num, stance in enumerate(self.stances):
            is_alive = self._get_agent_status(agent_num)
            if is_alive:
                self.alive.append(agent_num + 1)
            stance.update_alive(is_alive)

        # カラースケール情報の更新
        for agent_num, colour_scale in enumerate(self.colour_scales):
            colour_scale.update_alive(self._get_agent_status(agent_num))

        # カミングアウト情報の更新
        for agent_num, coming_out in enumerate(self.coming_outs):
            coming_out.update_alive(self._get_agent_status(agent_num))

        # 日付の更新
        if self.info is not None:
            self.day = int(self.info.day)

    @timeout
    def talk(self) -> str:
        if self.packet is not None:
            if self.talk_history is None:
                self.talk_history = self.packet.talk_history
            elif self.packet.talk_history is not None:
                self.talk_history.extend(self.packet.talk_history)
                MAX_HISTORY_LENGTH = 20  # 保持したい履歴の長さ
                if len(self.talk_history) > MAX_HISTORY_LENGTH:
                    # 後ろからMAX_HISTORY_LENGTH個の要素を取得
                    self.talk_history = self.talk_history[-MAX_HISTORY_LENGTH:]

        if self.day == 0:
            return "Over"

        # comment = random.choice(self.comments)  # noqa: S311

        # 他人のスタンスの更新
        self.update_stances()
        # 他人のカミングアウト状況の更新
        self.update_colour_scales()
        # 他人のカミングアウト状況の更新
        self.update_coming_outs()
        # 自分の戦略の更新
        self.update_my_tactics()
        # 発言（改行は含めない）
        comment = self.generate_statement().replace("\n", " ")

        self.save_talk_log(comment)

        if self.agent_log is not None:
            self.agent_log.talk(comment=comment)
        return comment

    def save_talk_log(self, statement: str):
        # 各部分を個別に作成して結合
        stances_text = "\n".join(
            [
                f"{stance.target_agent_id} - {stance.day_stances}"
                for stance in self.stances
            ]
        )
        colour_scales_text = "\n".join(
            [
                f"{colour_scale.target_agent_id} - {colour_scale.day_colour_scales}"
                for colour_scale in self.colour_scales
            ]
        )
        coming_outs_text = "\n".join(
            [
                f"{coming_out.target_agent_id} - {coming_out.day_coming_outs}"
                for coming_out in self.coming_outs
            ]
        )

        msg = f"""-----TALK-----
        --update stances--
        {stances_text}
        --update colour_scales--
        {colour_scales_text}
        --update coming_outs--
        {coming_outs_text}
        --update my_tactics--
        {self.my_tactics.tactics}
        --statement--
        {statement}
        --------------"""
        log(self.index, [msg])
        log_talk(self.index, self.role, statement)

    # @timeout
    # @send_agent_index
    # def vote(self) -> int:
    #     target: int = agent_util.agent_name_to_idx(
    #         name=random.choice(self.alive_agents),  # noqa: S311
    #     )
    #     if self.agent_log is not None:
    #         self.agent_log.vote(vote_target=target)
    #     return target

    # @timeout
    # def whisper(self) -> None:
    #     if self.packet is not None:
    #         if self.whisper_history is None:
    #             self.whisper_history = self.packet.whisper_history
    #         elif self.packet.whisper_history is not None:
    #             self.whisper_history.extend(self.packet.whisper_history)

    def update_stances(self):
        # スレッドプールエグゼキュータを使用して並列に処理
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 各スタンスの更新タスクをサブミット
            futures = [
                executor.submit(stance.update, self.day, self.talk_history)
                for stance in self.stances
            ]
            # 全てのタスクが完了するのを待つ
            concurrent.futures.wait(futures)

    def update_colour_scales(self):
        # スレッドプールエグゼキュータを使用して並列に処理
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 各スタンスの更新タスクをサブミット
            futures = [
                executor.submit(colour_scale.update, self.day, self.talk_history)
                for colour_scale in self.colour_scales
            ]
            # 全てのタスクが完了するのを待つ
            concurrent.futures.wait(futures)

    def update_coming_outs(self):
        # スレッドプールエグゼキュータを使用して並列に処理
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 各スタンスの更新タスクをサブミット
            futures = [
                executor.submit(coming_out.update, self.day, self.talk_history)
                for coming_out in self.coming_outs
            ]
            # 全てのタスクが完了するのを待つ
            concurrent.futures.wait(futures)

    def update_my_tactics(self):
        self.my_tactics.update(
            self.day,
            self.stances,
            self.colour_scales,
            self.coming_outs,
            self.alive_agents_num,
        )

    def generate_statement(self):
        return generate_statement(
            f"{int(self.index):02d}",
            self.role,
            self.talk_history,
            self.my_tactics,
        )

    # def decide_vote(self) -> int:
    #     return self.my_tactics.decide_vote_target(self.index, self.role, self.alive)

    def _get_formatted_agent_ids(self) -> list[str]:
        """
        エージェントIDのリストを整形された形式で取得する
        Returns:
            list[str]: 整形されたエージェントIDのリスト
        """
        if self.info is None:
            return []

        status_map = self.info.status_map
        return [
            f"{agent_util.agent_name_to_idx(name=agent_id):02d}"
            for agent_id in status_map.get_alive_agent_list()
        ]

    def init_stances(self):
        """
        スタンス情報を初期化
        """
        self.stances = [
            Stance(f"{int(self.index):02d}", self.role, agent_id)
            for agent_id in self._get_formatted_agent_ids()
        ]

    def init_colour_scales(self):
        """
        カラースケール情報を初期化
        """
        self.colour_scales = [
            Colour_Scale(f"{int(self.index):02d}", self.role, agent_id)
            for agent_id in self._get_formatted_agent_ids()
        ]

    def init_coming_outs(self):
        """
        カミングアウト情報を初期化
        """
        self.coming_outs = [
            Coming_Out(f"{int(self.index):02d}", self.role, agent_id)
            for agent_id in self._get_formatted_agent_ids()
        ]

    def init_tactics(self):
        """
        initializeを受け取ったタイミングで実行
        """
        self.my_tactics = MyTactics(
            day=0,  # 初期化時は0日目
            my_agent_id=f"{int(self.index):02d}",
            my_agent_role=self.role,
            roleNumMap=self.setting.role_num_map.__str__(),
        )

    def transfer_state(self, prev_agent: Agent) -> None:
        super().transfer_state(prev_agent)

        if isinstance(prev_agent, Agent_OpenAI):
            self.my_tactics = prev_agent.my_tactics
            self.stances = prev_agent.stances
            self.colour_scales = prev_agent.colour_scales
            self.coming_outs = prev_agent.coming_outs
            self.day = prev_agent.day

    # def action(self) -> str:  # noqa: C901
    #     if self.packet is None:
    #         return ""
    #     if self.packet.talk_history is not None:
    #         self.talk_history = self.packet.talk_history[:30]
    #     if Action.is_initialize(request=self.packet.request):
    #         self.initialize()
    #     elif Action.is_name(request=self.packet.request):
    #         return self.get_name()
    #     elif Action.is_role(request=self.packet.request):
    #         return self.get_role()
    #     elif Action.is_daily_initialize(request=self.packet.request):
    #         self.daily_initialize()
    #     elif Action.is_daily_finish(request=self.packet.request):
    #         self.daily_finish()
    #     elif Action.is_talk(request=self.packet.request):
    #         return self.talk()
    #     elif Action.is_vote(request=self.packet.request):
    #         return self.vote()
    #     elif Action.is_whisper(request=self.packet.request):
    #         self.whisper()
    #     elif Action.is_finish(request=self.packet.request):
    #         self.finish()
    #     return ""
