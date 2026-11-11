"""
시험 2회차 자동 채점기 - 수정 금지!

새로 나오는 문법:
    error.value.__cause__
        -> 'raise A from B'로 던진 예외 A에는 원인 예외 B가 __cause__에 기록된다.
    datetime(2026, 11, 7, 23, 59, tzinfo=KST)
        -> 글자를 해석하지 않고 숫자로 직접 날짜 객체를 만드는 방법
"""
import hashlib
from datetime import datetime, timedelta, timezone

import pytest

from q1_dates import DateFormatError, is_overdue, parse_korean_date
from q2_keys import find_new, make_key

KST = timezone(timedelta(hours=9))


# -- B1. 날짜 --

@pytest.mark.parametrize("text, expected", [
    ("2026년 11월 07일 23시 59분", "2026-11-07T23:59:00+09:00"),
    ("2026년 11월 08일 00시 00분", "2026-11-08T00:00:00+09:00"),        # 자정
    ("   2026년 01월 02일 09시 05분  ", "2026-01-02T09:05:00+09:00"),   # 앞뒤 공백
])
def test_b1_parse_korean_date(text, expected):
    assert parse_korean_date(text) == expected


@pytest.mark.parametrize("bad", [
    "2026-11-07 23:59",               # 모양이 다름
    "2026년 13월 01일 00시 00분",      # 13월은 없음
    "",                               # 빈 글자
])
def test_b1_bad_text_raises_date_format_error(bad):
    with pytest.raises(DateFormatError):
        parse_korean_date(bad)

def test_b1_error_message_shows_the_text():
    with pytest.raises(DateFormatError) as error:
        parse_korean_date("2026-11-07 23:59")
    assert "2026-11-07 23:59" in str(error.value)


def test_b1_error_keeps_original_cause():
    with pytest.raises(DateFormatError) as error:
        parse_korean_date("엉망")
    # raise DateFormatError(...) from e 라고 쓰면,
    # 새 예외 안에 "원래 원인은 e 였다."는 기록이 __cause__라는 칸에 저장됨.
    # 채점기는 이 칸에 ValueError가 들어 있는지 확인
    # 그래서 from e를 빼먹으면 이 테스트만 실패
    assert isinstance(error.value.__cause__, ValueError)


DUE = "2026-11-07T23:59:00+09:00"


# (지금 시각, 마감이 지났나?)
@pytest.mark.parametrize("now, expected", [
    (datetime(2026, 11, 7, 23, 58, tzinfo=KST), False),               # 1분 전
    (datetime(2026, 11, 7, 23, 59, tzinfo=KST), False),               # 정확히 마감 시각
    (datetime(2026, 11, 8, 0, 0, tzinfo=KST), True),                  # 1분 후
    (datetime(2026, 11, 7, 15, 0, tzinfo=timezone.utc), True),        # UTC 15:00 = KST 24:00
])
def test_b1_is_overdue(now, expected):
    # is expected(==가 아니라 is)
    # True와 False는 파이썬 안에 딱 하나씩만 존재함.
    # 그래서 is로 정확히 그 값인지를 확인함
    # is_overdue가 1이나 "yes"처럼 참 비슷한 값을 주면 is True에서 걸러짐
    # 진짜 bool을 돌려줘야 한다는 뜻
    assert is_overdue(DUE, now) is expected


# ────────────── B2. 키 ──────────────

ITEM = {"title": "과제1", "subject": "자료구조", "due": DUE}
FIELDS = ["title", "subject", "due"]


def test_b2_make_key_matches_sha256_of_joined_fields():
    expected = hashlib.sha256(f"과제1|자료구조|{DUE}".encode("utf-8")).hexdigest()
    assert make_key(ITEM, FIELDS) == expected
    assert len(make_key(ITEM, FIELDS)) == 64


def test_b2_field_order_matters():
    assert make_key(ITEM, ["title", "subject"]) != make_key(ITEM, ["subject", "title"])


def test_b2_only_listed_fields_are_used():
    # due가 달라도 fields에 due가 없으면 같은 키
    other = {**ITEM, "due": "2026-11-09T23:59:00+09:00"}
    assert make_key(ITEM, ["title", "subject"]) == make_key(other, ["title", "subject"])


def test_b2_missing_field_raises_key_error():
    with pytest.raises(KeyError):
        make_key({"title": "과제1"}, FIELDS)


def test_b2_find_new_skips_existing():
    a, b = ITEM, {**ITEM, "title": "과제2"}
    existing = {make_key(a, FIELDS)}
    assert find_new([a, b], existing, FIELDS) == [b]


def test_b2_find_new_removes_duplicates_in_same_batch():
    a, b = ITEM, {**ITEM, "title": "과제2"}
    assert find_new([a, b, dict(a)], set(), FIELDS) == [a, b]   # 순서 유지, 첫 번째만


def test_b2_find_new_does_not_change_existing():
    existing = set()
    find_new([ITEM], existing, FIELDS)
    assert existing == set()          # 넘겨준 set을 함수가 몰래 바꾸면 안 된다


def test_b2_find_new_empty():
    assert find_new([], set(), FIELDS) == []