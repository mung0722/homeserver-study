"""
B1. 한국어 날짜 해석기 - app/scraper.py의 convert_due_date 응용

규칙은 문제지(README.md) B1 참고
"""
from datetime import datetime, timedelta, timezone

# 한국 표준시
KST = timezone(timedelta(hours=9))

# TODO 1: DateFormatError 클래스 (Exception 상속)


def parse_korean_date(text: str) -> str:
    # TODO 2: 앞뒤 공백 제거

    # TODO 3: 글자 -> 날짜 객체 (형식 문자열은 직접 만들어보기)
    #       ValueError가 나면 DateFormatError로 바꿔서 던진다.
    #       (메시지에 공백 제거한 글자 포함, 원래 예외를 원인으로 연결)

    # TODO 4: 한국 시간대를 붙이고 ISO 문자열로 돌려준다.
    pass # 코드 작성 후 삭제 or 주석처리하여 없애기


def is_overdue(due_iso: str, now: datetime) -> bool:
    # TODO 5: ISO 글자 -> 날짜 객체로 바꾼 뒤, now가 마감보다 늦은지 비교해서 돌려줌
    #       (정확히 같은 시각은 False)
    pass # 코드 작성 후 삭제 or 주석처리하여 없애기