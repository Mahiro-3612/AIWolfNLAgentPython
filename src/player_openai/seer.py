from __future__ import annotations

import random

from aiwolf_nlp_common import Action

from player_openai.agent import Agent_OpenAI
from utils import agent_util


class Seer(Agent_OpenAI):
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

    @Agent_OpenAI.timeout
    def get_name(self) -> str:
        return super().get_name()

    @Agent_OpenAI.timeout
    def get_role(self) -> str:
        return super().get_role()

    @Agent_OpenAI.timeout
    def talk(self) -> str:
        return super().talk()

    @Agent_OpenAI.timeout
    def vote(self) -> int:
        return super().vote()

    @Agent_OpenAI.timeout
    def whisper(self) -> None:
        return super().whisper()

    @Agent_OpenAI.timeout
    @Agent_OpenAI.send_agent_index
    def divine(self) -> int:
        target: int = self.decide_divine()
        if self.agent_log is not None:
            self.agent_log.divine(divine_target=target)
        return target

    def decide_divine(self) -> int:
        return self.my_tactics.decide_divine_target(
            day=self.day,
            my_agent_id=self.index,
            alive_agents_list=self.alive_agents_list,
            stances=self.stances,
            colour_scales=self.colour_scales,
            coming_outs=self.coming_outs,
        )

    def action(self) -> str:
        if self.packet is not None and Action.is_divine(request=self.packet.request):
            return self.divine()
        return super().action()
