from player_openai.stance import Stance
from player_openai.colour_scale import Colour_Scale
from player_openai.coming_out import Coming_Out
from player_openai.langchain import OpenAIAgent
from player_openai.strategies import Base_Talk_Starategy
from typing import Dict, List
import sys

openai_agent = OpenAIAgent(temperature=1)


def get_tactic(
    day: int,
    my_agent_id: str,
    my_agent_role,
    roleNumMap: str,
    stances: list[Stance],
    prev_tactics: dict[int, str],
    alive_agents_num: int,
    alive_agents_list: list[str],
) -> str:
    # colour_scales: list[Colour_Scale],
    # coming_outs: list[Coming_Out],
    """
    戦略の更新
    args:
        - agent_id: 自分のエージェントID
        - stances: 各エージェントのスタンス(5人分)
    """

    base_talk_strategy = Base_Talk_Starategy()
    base_talk_strategy_str = base_talk_strategy.get_all_strategies()

    system = """
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
ゲームの参加者は全部で{alive_agents_num}人です。
あなたの役職は{my_agent_role}です。
今は{day}日目です。
また、各役職の人数は以下の通りです。
{roleNumMap}
生存者は以下の通りです。
{alive_agents_list}
行動を決める際の基本戦略は以下です。これを日付情報、自分の役職、与えられた役職カミングアウトの情報、市民陣営である確率の情報から参照して、戦略を立てる際のベースとしてください。
{base_talk_strategy_str}
このゲームは、初日の占いがあります。
"""

    template = """
# 指示
このプロンプトでは、あなたの現在のゲーム状況と他のエージェントとの相互作用を考慮して、効果的な戦略を生成することを目的としています。市民である確率や過去の戦略、現在のエージェントのスタンス、役職のカミングアウト状況を基に、次の行動計画を立ててください。
ただし、戦略を立てる際にはシステムプロンプト内の基本戦略をベースとし、そこから大きく逸脱しないようにしてください。

# タスク
1. 現在のゲーム状況を分析し、どのエージェントが最も影響力があるかを判断します。
2. 他のエージェントの役職推定とその根拠を考慮し、どのエージェントを支援または攻撃するかを決定します。
3. これまでの戦略と現在の状況を比較し、新たなアプローチを考案してください。

# 出力形式
- 出力は具体的な行動計画とその理由を含む形で整理してください。

# データ
- 各エージェントの発言のまとめ
{stances}
- 過去の戦略
{prev_tactics}
"""
    # - 各エージェントが市民陣営である確率
    # {colour_scales}
    # - 各エージェントの役職カミングアウト
    # {coming_outs}

    try:
        input = {
            "day": day,
            "my_agent_id": my_agent_id,
            "my_agent_role": my_agent_role.ja,
            "roleNumMap": roleNumMap,
            "stances": get_str_stances(stances),
            "prev_tactics": get_str_prev_tactics(prev_tactics),
            "alive_agents_num": alive_agents_num,
            "alive_agents_list": alive_agents_list,
            "base_talk_strategy_str": base_talk_strategy_str,
        }
        # "colour_scales": get_str_colour_scales(colour_scales),
        # "coming_outs": get_str_coming_outs(coming_outs),
        output = openai_agent.chat(system, template, input)

        return output
    except Exception as e:
        print("tactic error:", e)
        return ""


# def get_str_roleMap(roleNumMap: Dict[str, int]) -> str:
#     # MEMO: num > 0 のroleのみ表示
#     return " ".join([f"{role}: {num}" for role, num in roleNumMap.items() if num > 0])


def get_str_stance(stance: Stance) -> str:
    return "Agent_id: " + stance.target_agent_id + "Stances: " + str(stance.day_stances)


def get_str_stances(stances: list[Stance]) -> str:
    return " ".join([get_str_stance(stance) for stance in stances])


# def get_str_colour_scale(colour_scale: Colour_Scale) -> str:
#     return (
#         "Agent_id: "
#         + colour_scale.target_agent_id
#         + "Colour_Scales: "
#         + str(colour_scale.day_colour_scales)
#     )


# def get_str_colour_scales(colour_scales: list[Colour_Scale]) -> str:
#     return " ".join(
#         [get_str_colour_scale(colour_scale) for colour_scale in colour_scales]
#     )


# def get_str_coming_out(coming_out: Coming_Out) -> str:
#     return (
#         "Agent_id: "
#         + coming_out.target_agent_id
#         + "Coming_Outs: "
#         + str(coming_out.day_coming_outs)
#     )


# def get_str_coming_outs(coming_outs: list[Coming_Out]) -> str:
#     return " ".join([get_str_coming_out(coming_out) for coming_out in coming_outs])


def get_str_prev_tactics(prev_tactics: dict[int, str]):
    return " ".join(
        [f"day: {day}, tactic: {tactic}" for day, tactic in prev_tactics.items()]
    )
