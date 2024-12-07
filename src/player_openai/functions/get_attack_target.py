from player_openai.stance import Stance
from player_openai.colour_scale import Colour_Scale
from player_openai.coming_out import Coming_Out
from player_openai.langchain import OpenAIAgent
from player_openai.strategies import Base_Attack_Starategy
from pydantic import BaseModel
import random


class VoteTarget(BaseModel):
    target_id: int


openai_agent = OpenAIAgent(temperature=1)


def get_attack_target(
    day: int,
    my_agent_id: int,
    alive_agents: list[str],
    stances: list[Stance],
    colour_scales: list[Colour_Scale],
    coming_outs: list[Coming_Out],
) -> int:
    """
    襲撃先の決定

    Args:
        agent_id: 自分のエージェントID
        alive_agents: 生存者リスト
        my_tactics: 自分の日毎の戦略のリスト
    """
    base_attack_strategy = Base_Attack_Starategy()
    base_attack_strategy_str = base_attack_strategy.get_all_strategies()

    system = """
    あなたは人狼ゲームをプレイしています。
    襲撃するべきエージェントのidをintで指定して、数字のみを出力してください。（例：1）
    あなたの役職は人狼です。
    今は{day}日目です。
    生存者は以下の通りです。
    {alive_agents}
    行動を決める際の基本戦略は以下です。これを日付情報、自分の役職、与えられた役職カミングアウトの情報、市民陣営である確率の情報から参照して、戦略を立てる際のベースとしてください。
    {base_attack_strategy_str}
    """
    template = """
    あなたの名前はAgent[0{my_agent_id}]です。あなたの役職は人狼です。
    このゲームに勝利するために今日どのエージェントを襲撃するべきか、エージェントのidをintで指定して、数字のみを出力してください。（例：1）ただし、生存者のうちから自分以外のAgentを選ぶこと。

    - 各エージェントの発言のまとめ
    {stances}
    - 各エージェントが市民陣営である確率
    {colour_scales}
    - 各エージェントの役職カミングアウト
    {coming_outs}
    """

    input = {
        "day": day,
        "my_agent_id": my_agent_id,
        "alive_agents": alive_agents,
        "stances": get_str_stances(stances),
        "colour_scales": get_str_colour_scales(colour_scales),
        "coming_outs": get_str_coming_outs(coming_outs),
        "base_attack_strategy_str": base_attack_strategy_str,
    }

    # output: VoteTarget = openai_agent.json_mode_chat(
    #     system, template, input, pydantic_object=VoteTarget
    # )
    for _ in range(5):
        try:
            output = openai_agent.chat(system, template, input)
            # 整数への変換を試みる
            print("襲撃結果：", output)
            result = int(output)
            return result  # 成功したら即座に返す
        except ValueError:
            print("襲撃失敗！")
            continue

    return int(random.choice(alive_agents).split("[")[1].split("]")[0])


# def get_str_my_tactics(my_tactics: MyTactics):
#     return " ".join(
#         [f"day: {day}, tactic: {tactic}" for day, tactic in my_tactics.items()]
#     )


def get_str_stance(stance: Stance) -> str:
    return "Agent_id: " + stance.target_agent_id + "Stances: " + str(stance.day_stances)


def get_str_stances(stances: list[Stance]) -> str:
    return " ".join([get_str_stance(stance) for stance in stances])


def get_str_colour_scale(colour_scale: Colour_Scale) -> str:
    return (
        "Agent_id: "
        + colour_scale.target_agent_id
        + "Colour_Scales: "
        + str(colour_scale.day_colour_scales)
    )


def get_str_colour_scales(colour_scales: list[Colour_Scale]) -> str:
    return " ".join(
        [get_str_colour_scale(colour_scale) for colour_scale in colour_scales]
    )


def get_str_coming_out(coming_out: Coming_Out) -> str:
    return (
        "Agent_id: "
        + coming_out.target_agent_id
        + "Coming_Outs: "
        + str(coming_out.day_coming_outs)
    )


def get_str_coming_outs(coming_outs: list[Coming_Out]) -> str:
    return " ".join([get_str_coming_out(coming_out) for coming_out in coming_outs])
