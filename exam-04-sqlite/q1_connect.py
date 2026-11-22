"""
B1. 연결 도우미와 표 만들기 - lms-api/app/runs_db.py의 CREATE_TABLE_SQL, _connect 응용

규칙은 문제지(README.md) B1 참고
"""
import sqlite3
from contextlib import contextmanager


# TODO 1: loans 표를 만드는 SQL을 여러 줄 글자(""" """)로 쓴다.
#   - 이미 표가 있으면 넘어가야 한다.
#   - 열: id, title, borrower, borrowed_at, returned_at (타입/조건은 README 표 참고)
#   - 한 줄에 열 하나씩
CREATE_TABLE_SQL = """
"""


# TODO 2: 이 함수를 'with open_db(path) as conn:'으로 쓸 수 있게 만드는 장식(@...)을 붙인다.
def open_db(path):
    # TODO 3: 연결을 연다.

    # TODO 4: 행을 row["title"]처럼 열 이름으로 읽을 수 있게 설정한다.

    # TODO 5: 아래 동작을 만든다.
    #   - 연결 객체 자체를 with에 써서 '성공 -> commit / 에러 -> rollback'
    #   - 그 안에서 바깥 with 블록에 conn을 넘겨준다 (힌트: yield)
    #   - 에러가 나든 안 나든 '반드시' 연결을 닫는다 (힌트: try / finally)
    pass  # 코드 작성 후 삭제


def create_table(conn) -> None:
    # TODO 6: 받은 conn으로 CREATE_TABLE_SQL을 실행한다.
    pass  # 코드 작성 후 삭제
