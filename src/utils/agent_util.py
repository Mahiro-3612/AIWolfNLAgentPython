import re

from aiwolf_nlp_common.role import RoleInfo

import player_openai

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player_openai.agent import Agent_OpenAI


def set_role(
    prev_agent: "Agent_OpenAI",  # 文字列で型を指定
) -> "Agent_OpenAI":
    agent: player_openai.agent.Agent_OpenAI
    if RoleInfo.is_villager(role=prev_agent.role):
        agent = player_openai.villager.Villager()
    elif RoleInfo.is_werewolf(role=prev_agent.role):
        agent = player_openai.werewolf.Werewolf()
    elif RoleInfo.is_seer(role=prev_agent.role):
        agent = player_openai.seer.Seer()
    elif RoleInfo.is_possessed(role=prev_agent.role):
        agent = player_openai.possessed.Possessed()
    else:
        raise ValueError(prev_agent.role, "Role is not defined")
    agent.transfer_state(prev_agent=prev_agent)
    return agent


def agent_name_to_idx(name: str) -> int:
    match = re.search(r"\d+", name)
    if match is None:
        raise ValueError(name, "No number found in agent name")
    return int(match.group())


def agent_idx_to_agent(idx: int) -> str:
    return f"Agent_OpenAI[{idx:0>2d}]"
