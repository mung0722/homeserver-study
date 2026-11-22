"""
B2. 대출 장부 - lms-api/app/runs_db.py의 RunStore 응용

규칙은 문제지(README.md) B2 참고
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path

from q1_connect import create_table, open_db

KST = timezone(timedelta(hours=9))


def now_kst() -> datetime:
    """지금 이 순간의 한국 시간 (이미 완성됨)"""
    return datetime.now(KST)


class LoanBook:
    def __init__(self, db_path):
        # TODO 1: db_path를 Path 객체로 바꿔 속성 db_path에 저장한다.

        # TODO 2: DB 파일이 들어갈 폴더를 만든다. (중간 폴더까지, 이미 있으면 그냥 넘어가기)

        # TODO 3: open_db로 연결을 열고 create_table로 표를 만든다.
        pass  # 코드 작성 후 삭제

    def borrow(self, title: str, borrower: str) -> int:
        # TODO 4: borrowed_at = 지금 시각(ISO 글자)
        #         INSERT로 title, borrower, borrowed_at만 넣는다. (값은 모두 ? 로)
        #         lastrowid를 받고, None이면 RuntimeError를 던진다.
        #         그 id를 돌려준다.
        pass  # 코드 작성 후 삭제

    def get(self, loan_id: int) -> dict | None:
        # TODO 5: 그 id의 줄을 하나 꺼낸다.
        #         없으면 None, 있으면 진짜 딕셔너리로 바꿔서 돌려준다.
        pass  # 코드 작성 후 삭제

    def return_book(self, loan_id: int) -> bool:
        # TODO 6: '그 id' 이면서 '아직 반납 안 된' 줄만 returned_at을 지금 시각으로 고친다.
        #         (힌트: WHERE ... AND ...)
        #         실제로 고친 줄이 있으면 True, 없으면 False
        #         (힌트: 넘겨받은 loan_id가 아니라 'DB의 대답'으로 판단한다)
        pass  # 코드 작성 후 삭제

    def not_returned(self) -> list[dict]:
        # TODO 7: 반납 안 된 줄 전부를 id 작은 것부터 꺼내서
        #         딕셔너리 리스트로 돌려준다. (for / append)
        pass  # 코드 작성 후 삭제

    def latest(self, limit: int = 3) -> list[dict]:
        # TODO 8: 최근 줄을 최신순으로 최대 limit개 꺼내서
        #         딕셔너리 리스트로 돌려준다. (limit도 ? 로)
        pass  # 코드 작성 후 삭제
