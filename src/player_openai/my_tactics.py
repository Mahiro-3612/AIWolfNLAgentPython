from player_openai.stance import Stance
from player_openai.colour_scale import Colour_Scale
from player_openai.coming_out import Coming_Out
from player_openai.functions.get_tactic import get_tactic

from player_openai.functions.get_vote_target import get_vote_target
from player_openai.functions.get_attack_target import get_attack_target
from player_openai.functions.get_divine_target import get_divine_target
import random
from typing import Dict


class MyTactics:
    def __init__(
        self, day: int, my_agent_id: str, my_agent_role: str, roleNumMap: str
    ) -> None:
        self.day: int = day
        self.my_agent_id: str = my_agent_id
        self.my_agent_role: str = my_agent_role
        self.roleNumMap: str = roleNumMap
        self.tactics: dict[int, str] = {}

    def update(
        self,
        day: int,
        stances: list[Stance],
        alive_agents_num: int,
    ):
        # colour_scales: list[Colour_Scale],
        # coming_outs: list[Coming_Out],
        tactic: str = get_tactic(
            day,
            self.my_agent_id,
            self.my_agent_role,
            self.roleNumMap,
            stances,
            self.tactics,
            alive_agents_num,
        )
        # colour_scales,
        # coming_outs,

        self.tactics[day - 1] = tactic  # 同じ日のスタンスは上書き

    def decide_vote_target(
        self,
        day: int,
        my_agent_id: int,
        my_agent_role,
        alive_agents_list: list[str],
        stances: list[Stance],
    ) -> int:
        # colour_scales: list[Colour_Scale],
        # coming_outs: list[Coming_Out],
        for _ in range(5):
            target_id: int = get_vote_target(
                day,
                my_agent_id,
                my_agent_role,
                alive_agents_list,
                stances,
            )
            # colour_scales,
            # coming_outs,

            # target_idが生きているか
            if f"Agent[{int(target_id):02d}]" not in alive_agents_list:
                continue

            # target_idが自分自身でないか
            if f"Agent[{int(target_id):02d}]" == my_agent_id:
                continue

            return target_id
        # print("Error: 5回試行しても投票先が決まらなかった")
        target = random.choice(alive_agents_list)
        # print(f"ランダムに投票先を決定: 自分のid: {agent_id}, target: {target}")
        target_id = int(target.split("[")[1].split("]")[0])

        return target_id

    def decide_attack_target(
        self,
        day: int,
        my_agent_id: int,
        alive_agents_list: list[str],
        stances: list[Stance],
    ) -> int:
        # colour_scales: list[Colour_Scale],
        # coming_outs: list[Coming_Out],
        for _ in range(5):
            target_id: int = get_attack_target(
                day,
                my_agent_id,
                alive_agents_list,
                stances,
            )
            # colour_scales,
            # coming_outs,

            # target_idが生きているか
            if f"Agent[{int(target_id):02d}]" not in alive_agents_list:
                continue

            # target_idが自分自身でないか
            if f"Agent[{int(target_id):02d}]" == my_agent_id:
                continue

            return target_id
        # print("Error: 5回試行しても攻撃先が決まらなかった")
        target = random.choice(alive_agents_list)
        # print(f"ランダムに投票先を決定: 自分のid: {agent_id}, target: {target}")
        target_id = int(target.split("[")[1].split("]")[0])

        return target_id

    def decide_divine_target(
        self,
        day: int,
        my_agent_id: int,
        alive_agents_list: list[str],
        stances: list[Stance],
    ) -> int:
        # colour_scales: list[Colour_Scale],
        # coming_outs: list[Coming_Out],
        for _ in range(5):
            target_id: int = get_divine_target(
                day,
                my_agent_id,
                alive_agents_list,
                stances,
            )
            # colour_scales,
            # coming_outs,

            # target_idが生きているか
            if f"Agent[{int(target_id):02d}]" not in alive_agents_list:
                continue

            # target_idが自分自身でないか
            if f"Agent[{int(target_id):02d}]" == my_agent_id:
                continue

            return target_id
        # print("Error: 5回試行しても占い先が決まらなかった")
        target = random.choice(alive_agents_list)
        # print(f"ランダムに投票先を決定: 自分のid: {agent_id}, target: {target}")
        target_id = int(target.split("[")[1].split("]")[0])

        return target_id
