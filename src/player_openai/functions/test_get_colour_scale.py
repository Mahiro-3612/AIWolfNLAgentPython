from player_openai.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=1)


system = """
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
あなたの役職は{my_agent_role}です。
"""

template = """
# 指示
このプロンプトでは、人狼ゲームにおける特定のエージェント（Agent[{target_agent_id}]）の発言と行動、また占い結果などから、対象エージェントが市民陣営である確率がどれくらいかを判定します。

# 注意点
Agent[{target_agent_id}]がまだ発言、占いなどされていない場合、記録は行わないでください。その場合出力は空欄("")としてください。
範囲を持たせず、数字％の形で出力してください。（例：30%）

# データ
- 発言履歴
{talk_history}

# タスク
対象エージェントAgent[{target_agent_id}]が他のエージェントに関してどのような発言をしているか、どのような役職をカミングアウトしているか、また占い師（SEER）にどのように占われているかに注目して、対象エージェントが市民陣営である確率がどれくらいかを判定してください。
例えば、占い師とカミングアウトしている人が一人の場合は、市民陣営である確率は、カミングアウトした占い師: 100%, 'HUMAN'と占われたエージェント: 100%, 'WEREWOLF'と占われたエージェント: 0%, 'WEREWOLF'が確定していない状況で、占われていないエージェント": 66%となる。
例えば、占い師とカミングアウトしている人が二人でどちらも生きている場合は、市民陣営である確率は、どちらにも'HUMAN'と占われたエージェント: 100%, どちらにも'WEREWOLF'と占われたエージェント: 0%, 他のエージェント: 20%から25%となる。

# 出力形式
- 市民陣営である確率: 対象エージェントが市民陣営である確率を0%から100%で記してください。
"""

try:
    input = {
        "my_agent_id": "02",
        "my_agent_role": "狂人",
        "target_agent_id": "03",
        "day_colour_scale": "{}",
        "talk_history": "Agent[01]]\nOver\nAgent[03]]\nOver\nAgent[05]]\nOver\nAgent[04]]\nOver\nAgent[02]]\nOver",
    }
    output = openai_agent.chat(system, template, input)

except Exception as e:
    print("colour error:", e)
