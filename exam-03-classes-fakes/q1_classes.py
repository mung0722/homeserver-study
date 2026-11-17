"""
B1. 도장 카드 - 클래스 기초 (__init__, self, 속성, 메서드)

규칙은 문제지(README.md) B1 참고
"""


class StampCard:
    def __init__(self, owner: str, goal: int = 10):
        # TODO 1: owner, goal을 '이 객체의' 속성으로 저장한다.
        self.owner = owner
        self.goal = goal

        # TODO 2: stamps 속성을 0으로 시작한다.
        self.stamps = 0

        # pass  # 코드 작성 후 삭제

    def stamp(self, n: int = 1) -> bool:
        # TODO 3: n이 0 이하면 ValueError를 던진다. (도장 수를 바꾸기 '전에' 검사해야 한다)
        if n <= 0:
            raise ValueError("0이하")

        # TODO 4: stamps에 n을 더한다.
        self.stamps = self.stamps + n

        # TODO 5: stamps가 goal 이상이면 True, 아니면 False를 돌려준다.
        return self.stamps >= self.goal
        # pass  # 코드 작성 후 삭제

    def reset(self) -> None:
        # TODO 6: stamps를 0으로 되돌린다.
        self.stamps = 0
        # pass  # 코드 작성 후 삭제
