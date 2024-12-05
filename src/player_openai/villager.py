from __future__ import annotations

from player_openai.agent import Agent_OpenAI


class Villager(Agent_OpenAI):

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

    def action(self) -> str:
        return super().action()
