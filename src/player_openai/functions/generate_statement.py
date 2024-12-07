from player_openai.langchain import OpenAIAgent
from player_openai.my_tactics import MyTactics

openai_agent = OpenAIAgent(temperature=1)


def generate_statement(
    my_agent_id: str,
    alive_agents_num: int,
    my_agent_role,
    day: int,
    alive_agents_list: list[str],
    talk_history,
    my_tactics: MyTactics,
) -> str:
    """
    実際の発言を出力
    """

    system = """
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
ゲームの参加者は全部で{alive_agents_num}人です。
あなたの役職は{my_agent_role}です。
今は{day}日目です。
生存者は以下の通りです。
{alive_agents_list}
発言は簡潔かつ自然にしましょう。友達と話すような言葉遣いが望ましいです。
出力は50文字以内に納めましょう。
「>>Agent[01] 」というようなアンカーをtalkの発言冒頭につけることで、特定のエージェントに向けた発話ができます。発話を向けられたエージェントは、なにか応答することが期待されます。
このゲームは、初日の占いがあります。
"""

    template = """
# 指示
あなたは人狼ゲームをプレイしており、最新の戦略を踏まえた発言を生成することが目的です。直前の会話内容と一致し、かつ戦略的な意図を持った発言を作成してください。

# 注意点
- 出力はそのまま発言として使用されるため、発言以外の情報は含めないでください。
- 発言は簡潔かつ明確に、ゲーム内での自然な会話として整理してください。
- 出力は50文字以内に納めましょう。

# タスク
1. 直前の会話内容を分析し、そのトピックやトーンに基づいて発言を構築します。
2. あなたの戦略に基づいて、どのプレイヤーにどのようなメッセージを伝えるかを決定します。
3. 会話が自然であるように、過去の戦略や会話履歴から適切な情報を引用または参照し、新しい発言を形成します。

# データ
- 最新の戦略: {my_tactics}
- 直前の会話履歴: {talk_history}
"""

    try:
        input = {
            "my_agent_id": my_agent_id,
            "alive_agents_num": alive_agents_num,
            "my_agent_role": my_agent_role.ja,
            "day": day,
            "alive_agents_list": alive_agents_list,
            "talk_history": get_str_talk_history(talk_history),
            "my_tactics": get_str_my_tactics(my_tactics),
        }

        output = openai_agent.chat(system, template, input)
        return output
    except Exception as e:
        print("generate error:", e)
        return "発言の生成に失敗しました"


def get_str_my_tactics(my_tactics: MyTactics):
    my_day_tactics: dict[int, str] = my_tactics.tactics
    return " ".join(
        [f"day: {day}, tactic: {tactic}" for day, tactic in my_day_tactics.items()]
    )


def get_str_talk_history(talk_history) -> str:
    # MEMO: f-stringで書きたいが、[]をエスケープする必要があるため、+演算子で結合
    return "\n".join([str(talk.agent) + "]\n" + talk.text for talk in talk_history])
