from __future__ import annotations

import random

from aiwolf_nlp_common import Action

from player_openai.agent import Agent
from utils import agent_util
from player_openai.functions.generate_statement import generate_statement


class Seer(Agent):
    alive_agents_list: list[str]

    def __init__(self) -> None:
        super().__init__()

    def append_recv(self, recv: str | list[str]) -> None:
        return super().append_recv(recv)

    def set_packet(self) -> None:
        return super().set_packet()

    def initialize(self) -> None:
        return super().initialize()

    def daily_initialize(self) -> None:
        return super().daily_initialize()

    def daily_finish(self) -> None:
        return super().daily_finish()

    @Agent.timeout
    def get_name(self) -> str:
        return super().get_name()

    @Agent.timeout
    def get_role(self) -> str:
        return super().get_role()

    @Agent.timeout
    def talk(self) -> str:
        self.divine_result_str = self.info.divine_result.__str__()
        if self.packet is not None:
            if self.talk_history is None:
                self.talk_history = self.packet.talk_history
            elif self.packet.talk_history is not None:
                self.talk_history.extend(self.packet.talk_history)
                MAX_HISTORY_LENGTH = 10  # 保持したい履歴の長さ
                if len(self.talk_history) > MAX_HISTORY_LENGTH:
                    # 後ろからMAX_HISTORY_LENGTH個の要素を取得
                    self.talk_history = self.talk_history[-MAX_HISTORY_LENGTH:]

        if self.day == 0:
            return "Over"

        # comment = random.choice(self.comments)  # noqa: S311
        try:
            # 他人のスタンスの更新
            self.update_stances()
            # # # 他人のカミングアウト状況の更新
            # # self.update_colour_scales()
            # # # 他人のカミングアウト状況の更新
            # # self.update_coming_outs()
            # 自分の戦略の更新
            self.update_my_tactics()
            # 発言（改行は含めない）
            comment = self.generate_statement().replace("\n", " ")
            # comment = "あ"

            if self.agent_log is not None:
                self.agent_log.talk(comment=comment)
            return comment
        except:
            return "体調悪いので発言できません。"

    def generate_statement(self):
        if self.day == 1:
            return generate_statement(
                f"{int(self.index):02d}",
                self.alive_agents_num,
                self.role,
                self.day,
                self.alive_agents_list,
                self.divine_result_str,
                None,
                None,
                self.talk_history,
                self.my_tactics,
            )
        else:
            self.executed_agents = self.info.executed_agent.__str__()
            self.attacked_agents = self.info.attacked_agent.__str__()
            return generate_statement(
                f"{int(self.index):02d}",
                self.alive_agents_num,
                self.role,
                self.day,
                self.alive_agents_list,
                self.divine_result_str,
                self.executed_agents,
                self.attacked_agents,
                self.talk_history,
                self.my_tactics,
            )

    @Agent.timeout
    def vote(self) -> int:
        return super().vote()

    @Agent.timeout
    def whisper(self) -> None:
        return super().whisper()

    @Agent.timeout
    @Agent.send_agent_index
    def divine(self) -> int:
        target: int = self.decide_divine()
        if self.agent_log is not None:
            self.agent_log.divine(divine_target=target)
        return target

    def decide_divine(self) -> int:
        self.update_stances()
        self.update_my_tactics()
        return self.my_tactics.decide_divine_target(
            day=self.day,
            my_agent_id=self.index,
            alive_agents_list=self.alive_agents_list,
            stances=self.stances,
        )
        # colour_scales=self.colour_scales,
        # coming_outs=self.coming_outs,

    def action(self) -> str:
        if self.packet is not None:
            self.info = self.packet.info
            if Action.is_divine(request=self.packet.request):
                return self.divine()
        return super().action()
