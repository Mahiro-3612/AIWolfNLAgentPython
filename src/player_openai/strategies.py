class Base_Talk_Starategy:
    def __init__(
        self,
    ) -> None:
        self.STRATEGIES = {
            "1日目": {
                "自分の役職：村人": {
                    "占い師カミングアウトなし": {
                        "占い師がカミングアウトするように促す"
                    },
                    "占い師カミングアウト一人": {
                        "占い師を信用し、占い師が'人狼'と判定した人に投票するように、'市民'と判定した人に投票しないように促す"
                    },
                    "占い師カミングアウト二人": {
                        "できるだけ処刑されないように、様子を見る"
                    },
                },
                "自分の役職：人狼": {
                    "占い師カミングアウトなし": {
                        "できるだけ処刑されないように、様子を見る"
                    },
                    "占い師カミングアウト一人": {
                        "対抗で占い師とカミングアウトする。占い師が占ったエージェントとは別のエージェントの占い結果を共有する。相手の占い結果が'市民'なら同じく'市民'、'人狼'なら同じく'人狼'と占う"
                    },
                    "占い師カミングアウト二人": {
                        "できるだけ処刑されないように、様子を見る"
                    },
                },
                "自分の役職：狂人": {
                    "占い師カミングアウトなし": {
                        "できるだけ処刑されないように、様子を見る"
                    },
                    "占い師カミングアウト一人": {
                        "対抗で占い師とカミングアウトする。占い師が占ったエージェントとは別のエージェントの占い結果を共有する。相手の占い結果が'市民'なら同じく'市民'、'人狼'なら同じく'人狼'と占う"
                    },
                    "占い師カミングアウト二人": {
                        "できるだけ処刑されないように、様子を見る"
                    },
                },
                "自分の役職：占い師": {
                    "占い師カミングアウトなし": {
                        "できるだけ早く自分が占い師だとカミングアウトし、占い結果を共有する。"
                    },
                    "占い師カミングアウト一人": {
                        "まだカミングアウトしていない場合は、できるだけ早く自分が占い師だとカミングアウトし、占い結果を共有する。"
                    },
                    "占い師カミングアウト二人": {
                        "まだカミングアウトしていない場合は、できるだけ早く自分が占い師だとカミングアウトし、占い結果を共有する。"
                    },
                },
            },
            "2日目": {
                "自分の役職：村人": {
                    "占いなどの結果から、一番人狼陣営っぽいAgentに投票するよう促す。"
                },
                "自分の役職：人狼": {
                    "自分が占いカミングアウトしている場合は、できるだけ早く占い結果を共有する。占いなどの結果から、一番市民陣営っぽいAgentに投票するよう促す。"
                },
                "自分の役職：狂人": {
                    "自分が占いカミングアウトしている場合は、できるだけ早く占い結果を共有する。自分が狂人であることを伝え、人狼Agentに人狼をカミングアウトするように促す。そのエージェントと協力して同じエージェントに投票する。"
                },
                "自分の役職：占い師": {
                    "できるだけ早く占い結果を共有する。占いなどの結果から、一番人狼陣営っぽいAgentに投票するよう促す。"
                },
            },
        }

    def get_all_strategies(self) -> str:
        """
        全ての戦略を文字列として取得する
        """
        result = str(self.STRATEGIES)
        return result


class Base_Vote_Starategy:
    def __init__(
        self,
    ) -> None:
        self.STRATEGIES = {
            "1日目": {
                "自分の役職：村人": {
                    "占い師と、村人と占われた人以外で一番人狼陣営っぽいAgentを選ぶ。"
                },
                "自分の役職：人狼": {
                    "市民陣営が確定しているAgent、カミングアウトした占い師のAgentの順番に選ぶ。"
                },
                "自分の役職：狂人": {
                    "市民陣営が確定しているAgent、カミングアウトした占い師のAgentの順番に選ぶ。"
                },
                "自分の役職：占い師": {
                    "占い師と、村人と占われた人以外で一番人狼陣営っぽいAgentを選ぶ。"
                },
            },
            "2日目": {
                "自分の役職：村人": {
                    "占い師と、村人と占われた人以外で一番人狼陣営っぽいAgentを選ぶ。"
                },
                "自分の役職：人狼": {
                    "市民陣営が確定しているAgent、カミングアウトした占い師のAgentの順番に選ぶ。"
                },
                "自分の役職：狂人": {
                    "市民陣営が確定しているAgent、カミングアウトした占い師のAgentの順番に選ぶ。"
                },
                "自分の役職：占い師": {
                    "占い師と、村人と占われた人以外で一番人狼陣営っぽいAgentを選ぶ。"
                },
            },
        }

    def get_all_strategies(self) -> str:
        """
        全ての戦略を文字列として取得する
        """
        result = str(self.STRATEGIES)
        return result


class Base_Attack_Starategy:
    def __init__(
        self,
    ) -> None:
        self.STRATEGIES = {
            "真の占い師だと確定している占い師Agent、議論を前に進めているAgentなどから順に襲撃していく。"
        }

    def get_all_strategies(self) -> str:
        """
        全ての戦略を文字列として取得する
        """
        result = str(self.STRATEGIES)
        return result


class Base_Divine_Starategy:
    def __init__(
        self,
    ) -> None:
        self.STRATEGIES = {"人狼陣営だと疑わしいAgentから占っていく。"}

    def get_all_strategies(self) -> str:
        """
        全ての戦略を文字列として取得する
        """
        result = str(self.STRATEGIES)
        return result
