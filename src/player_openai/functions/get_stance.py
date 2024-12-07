from player_openai.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=1)


def get_stance(
    my_agent_id: str,
    my_agent_role,
    target_agent_id: str,
    day_stances: dict[int, str],
    talk_history,
) -> str:
    """
    他のエージェントのスタンスをまとめる

    Args:
        my_agent_id (str): 自分のエージェントID
        my_agent_role (str): 自分の役職
        target_agent_id (str): 対象のエージェントID
        day_stances (dict[int, str]): 日毎のスタンス
        talk_history: 発言履歴

    Returns:
        str: その日の、この関数を呼び出した時点での対象エージェントのカミングアウト状況
    """

    system = """
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
あなたの役職は{my_agent_role}です。
出力はできるだけ簡潔にまとめてください。
"""

    template = """
# 指示
このプロンプトでは、人狼ゲームにおける特定のエージェント（Agent[{target_agent_id}]）の発言と行動から情報を抽出し、そのエージェントのスタンスを評価します。対象エージェントの行動、役職推測、同意・非同意の表明などから、そのエージェントの意図や戦略を理解し、自エージェントの戦略に反映させる必要があります。

# 注意点
Agent[{target_agent_id}]がまだ発言していない場合、まとめは行わないでください。その場合出力は空欄としてください。

# タスク
1. 対象エージェントAgent[{target_agent_id}]の発言から、他のエージェントとの同意または非同意の動向を特定し、その背後にある意図や戦略を評価してください。
2. 対象エージェントAgent[{target_agent_id}]が他のエージェントに関してどのような発言をしているかに注目し、役職推測や戦略に関する言及を特定してください。
3. 対象エージェントAgent[{target_agent_id}]の発言から、役職のカミングアウト状況を辞書型で記録してください。
4. 対象エージェントAgent[{target_agent_id}]がどのような発言をしているか、どのような役職をカミングアウトしているか、また占い師にどのように占われているかに注目して、対象エージェントが市民陣営である確率がどれくらいかを判定してください。例えば、占い師とカミングアウトしている人が一人の場合は、市民陣営である確率は、カミングアウトした占い師: 100%, '市民'と占われたエージェント: 100%, '人狼'と占われたエージェント: 0%, '人狼'が確定していない状況で、占われていないエージェント": 66%となる。
例えば、占い師とカミングアウトしている人が二人でどちらも生きている場合は、市民陣営である確率は、どちらにも'市民'と占われたエージェント: 100%, どちらにも'人狼'と占われたエージェント: 0%, 他のエージェント: 20%から25%となる。

# 出力形式
- 同意または非同意の行動: [対象エージェントが他のエージェントに同意または非同意を示した具体的な発言を引用し、その背後にある意図や戦略を簡潔に解説してください。]
- 戦略予測: [対象エージェントの行動や発言から推測される戦略やその役職に基づいた行動指針を簡潔に説明してください。]
- 役職カミングアウト状況:　[対象エージェントの行動や発言から役職のカミングアウト状況を辞書型で記録してください。]（例："Agent01":"占い師カミングアウト"）
- 市民陣営である確率： [対象エージェントが市民陣営である確率がどれくらいかを0%から100%で判定してください。]（例："Agent01":50%）

# データ
- 発言履歴
{talk_history}
"""

    try:
        input = {
            "my_agent_id": my_agent_id,
            "my_agent_role": my_agent_role.ja,
            "target_agent_id": target_agent_id,
            "day_stances": get_str_day_stances(day_stances),
            "talk_history": get_str_talk_history(talk_history),
        }

        output = openai_agent.chat(system, template, input)

        return output
    except Exception as e:
        print("stance error:", e)
        return ""


def get_str_day_stances(day_stances: dict[int, str]) -> str:
    return str(day_stances)


def get_str_talk_history(talk_history) -> str:
    # MEMO: f-stringで書きたいが、[]をエスケープする必要があるため、+演算子で結合
    return "\n".join([str(talk.agent) + "]\n" + talk.text for talk in talk_history])
