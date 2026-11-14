"""
B1. 한국어 날짜 해석기 - app/scraper.py의 convert_due_date 응용

규칙은 문제지(README.md) B1 참고
"""
from datetime import datetime, timedelta, timezone

# 한국 표준시
KST = timezone(timedelta(hours=9))

# TODO 1: DateFormatError 클래스 (Exception 상속)
class DateFormatError(Exception):
    pass


def parse_korean_date(text: str) -> str:
    # TODO 2: 앞뒤 공백 제거
    text = text.strip()

    # TODO 3: 글자 -> 날짜 객체 (형식 문자열은 직접 만들어보기)
    #       ValueError가 나면 DateFormatError로 바꿔서 던진다.
    #       (메시지에 공백 제거한 글자 포함, 원래 예외를 원인으로 연결)
    try: 
        due = datetime.strptime(text, "%Y년 %m월 %d일 %H시 %M분")    
    except ValueError as e:
        # except 블록: try 안에서 ValueError가 '났을 때만' 실행됨
        # as e -> 실제로 발생한 예외 객체에 e라는 이름을 붙임
        # from e -> 새 예외의 __cause__에 e를 기록 ("원래 원인은 이거였다.")
        # 메시지에 공백 제거한 원래 글자를 넣는다 (!r -> 따옴표까지 보여 줘서 빈 글자도 눈에 보임)
        raise DateFormatError(f"날짜 형식이 맞지 않음: {text!r}") from e

    # TODO 4: 한국 시간대를 붙이고 ISO 문자열로 돌려준다.
    due = due.replace(tzinfo=KST)
    return due.isoformat()

    # pass # 코드 작성 후 삭제 or 주석처리하여 없애기

def is_overdue(due_iso: str, now: datetime) -> bool:
    # TODO 5: ISO 글자 -> 날짜 객체로 바꾼 뒤, now가 마감보다 늦은지 비교해서 돌려줌
    #       (정확히 같은 시각은 False)
    due = datetime.fromisoformat(due_iso)
    return now > due # 비교 결과를 그대로 돌려줌
    # pass # 코드 작성 후 삭제 or 주석처리하여 없애기