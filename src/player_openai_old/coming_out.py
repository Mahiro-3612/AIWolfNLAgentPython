from player_openai_old.info_types import TalkHistory, GameInfo
from player_openai_old.functions.get_coming_outs import get_coming_outs


class Coming_Out:
    """
    他プレイヤーのカミングアウト状況
    """

    def __init__(
        self, my_agent_id: str, my_agent_role: str, target_agent_id: str
    ) -> None:
        # 基本情報
        self.target_agent_id: str = target_agent_id
        self.my_agent_id: str = my_agent_id
        self.my_agent_role: str = my_agent_role
        self.alive: bool = True
        # 考察
        self.day_coming_outs: dict[int, str] = {}  # 日毎のカミングアウト状況のまとめ
        # self.habit = None

    def update_alive(self, alive: bool) -> None:
        self.alive = alive

    def update(self, day: int, talk_history: TalkHistory) -> None:
        if not self.alive:
            return

        # 最初の発言の場合はupdate不要
        if len(talk_history) == 0:
            return

        coming_out: str = get_coming_outs(
            self.my_agent_id,
            self.my_agent_role,
            self.target_agent_id,
            self.day_coming_outs,
            talk_history,
        )

        # 同じ日のスタンスを上書き
        self.day_coming_outs[day - 1] = coming_out
