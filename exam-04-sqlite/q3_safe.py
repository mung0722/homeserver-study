"""
B3. 안전한 검색과 시간 계산

규칙은 문제지(README.md) B3 참고
"""
from datetime import datetime


# ⚠️ 위험한 버전 (따라 쓰지 말 것!) - 이걸 안전하게 바꾸는 게 문제다
#
# def find_by_borrower(conn, name):
#     cursor = conn.execute(
#         f"SELECT title FROM loans WHERE borrower = '{name}' ORDER BY id"
#     )
#     ...


def find_by_borrower(conn, name: str) -> list[str]:
    # TODO 1: name을 ? 자리로 넘겨서 그 사람이 빌린 책의 title만 꺼낸다.
    #         id 작은 것부터. SQL은 한 줄에 한 절씩.

    # TODO 2: 꺼낸 줄마다 row["title"]을 새 리스트에 담아 돌려준다. (for / append)
    pass  # 코드 작성 후 삭제


def hours_between(start_iso: str, end_iso: str) -> float:
    # TODO 3: 두 글자를 각각 날짜 객체로 바꾼다.

    # TODO 4: 끝 - 시작 = 걸린 시간(timedelta)

    # TODO 5: 걸린 시간을 '시간' 단위 숫자로 바꾸고 (힌트: 초 / 3600)
    #         소수 첫째 자리까지 반올림해서 돌려준다.
    pass  # 코드 작성 후 삭제
