"""
시험 4회차 자동 채점기 - 수정 금지!

새로 나오는 문법:
    tmp_path
        -> pytest가 테스트마다 새로 주는 빈 임시 폴더 (매개변수 이름만 적으면 자동으로 들어옴)
    pytest.raises(A) as info
        -> 에러가 나면 그 정보를 info에 담아 둔다. (여기서는 안 씀)
    sqlite3.ProgrammingError
        -> 이미 닫힌 연결을 쓰려고 하면 나는 에러
"""
import sqlite3
from datetime import datetime
from pathlib import Path

import pytest

from q1_connect import CREATE_TABLE_SQL, create_table, open_db
from q2_loans import LoanBook
from q3_safe import find_by_borrower, hours_between


def insert_sample(conn, title, borrower, returned_at=None):
    """채점용 도우미: 표에 줄 하나를 직접 넣는다."""
    conn.execute(
        """
        INSERT INTO loans (
            title,
            borrower,
            borrowed_at,
            returned_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            title,
            borrower,
            "2026-11-01T09:00:00+09:00",
            returned_at,
        ),
    )


# -- B1. 연결 도우미와 표 만들기 --

def test_b1_create_table_columns(tmp_path):
    conn = sqlite3.connect(tmp_path / "t.db")
    conn.execute(CREATE_TABLE_SQL)
    conn.execute(CREATE_TABLE_SQL)    # 두 번 실행해도 에러가 나면 안 된다 (IF NOT EXISTS)

    # PRAGMA table_info: 표의 열 정보를 보여 주는 SQLite 명령
    #   각 줄: (번호, 이름, 타입, NOT NULL 여부, 기본값, 기본 키 여부)
    columns = {}
    for row in conn.execute("PRAGMA table_info(loans)"):
        columns[row[1]] = row
    conn.close()

    assert list(columns) == [
        "id",
        "title",
        "borrower",
        "borrowed_at",
        "returned_at",
    ]
    assert columns["id"][2] == "INTEGER"
    assert columns["id"][5] == 1               # 기본 키
    assert columns["title"][3] == 1            # NOT NULL
    assert columns["borrower"][3] == 1
    assert columns["borrowed_at"][3] == 1
    assert columns["returned_at"][3] == 0      # 비어 있어도 됨


def test_b1_autoincrement(tmp_path):
    conn = sqlite3.connect(tmp_path / "t.db")
    conn.execute(CREATE_TABLE_SQL)
    sql = conn.execute(
        "SELECT sql FROM sqlite_master WHERE name = 'loans'"
    ).fetchone()[0]
    conn.close()
    assert "AUTOINCREMENT" in sql.upper()


def test_b1_open_db_commits_and_row_factory(tmp_path):
    path = tmp_path / "t.db"
    with open_db(path) as conn:
        create_table(conn)
        insert_sample(conn, "파이썬", "민수")

    # 새로 열어도 남아 있어야 한다 -> commit 되었다는 뜻
    with open_db(path) as conn:
        row = conn.execute("SELECT * FROM loans").fetchone()

    assert row["title"] == "파이썬"           # 열 이름으로 읽기 (row_factory)


def test_b1_open_db_rolls_back_on_error(tmp_path):
    path = tmp_path / "t.db"
    with open_db(path) as conn:
        create_table(conn)

    with pytest.raises(RuntimeError):
        with open_db(path) as conn:
            insert_sample(conn, "파이썬", "민수")
            raise RuntimeError("중간에 에러!")

    with open_db(path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM loans").fetchone()[0]

    assert count == 0                          # 에러가 났으니 넣은 줄이 취소되어야 한다


def test_b1_open_db_closes_connection(tmp_path):
    path = tmp_path / "t.db"

    with open_db(path) as conn:
        pass
    with pytest.raises(sqlite3.ProgrammingError):
        conn.execute("SELECT 1")               # 성공한 뒤에도 닫혀 있어야 한다

    with pytest.raises(ValueError):
        with open_db(path) as conn2:
            raise ValueError("앗")
    with pytest.raises(sqlite3.ProgrammingError):
        conn2.execute("SELECT 1")              # 에러가 난 뒤에도 닫혀 있어야 한다


# -- B2. 대출 장부 --

def test_b2_init_makes_folder_and_table(tmp_path):
    path = tmp_path / "a" / "b" / "loans.db"   # 중간 폴더 a/b가 아직 없음
    book = LoanBook(str(path))                 # 글자 경로로 줘도 된다

    assert isinstance(book.db_path, Path)
    assert book.db_path == path
    assert path.exists()

    LoanBook(path)                             # 두 번 만들어도 에러가 나면 안 된다


def test_b2_borrow_and_get(tmp_path):
    book = LoanBook(tmp_path / "loans.db")
    first = book.borrow("파이썬", "민수")
    second = book.borrow("SQL", "지수")

    assert first == 1
    assert second == 2

    row = book.get(second)
    assert type(row) is dict                   # sqlite3.Row가 아니라 '진짜' dict
    assert row["title"] == "SQL"
    assert row["borrower"] == "지수"
    assert row["returned_at"] is None
    datetime.fromisoformat(row["borrowed_at"]) # ISO 글자로 저장되어 있어야 한다


def test_b2_get_missing_returns_none(tmp_path):
    book = LoanBook(tmp_path / "loans.db")
    loan_id = book.borrow("파이썬", "민수")
    assert book.get(loan_id) is not None       # 있는 번호는 찾고
    assert book.get(99) is None                # 없는 번호는 None


def test_b2_return_book(tmp_path):
    book = LoanBook(tmp_path / "loans.db")
    loan_id = book.borrow("파이썬", "민수")

    assert book.return_book(loan_id) is True   # 처음 반납 -> True
    returned_at = book.get(loan_id)["returned_at"]
    assert returned_at
    datetime.fromisoformat(returned_at)

    assert book.return_book(loan_id) is False  # 이미 반납됨 -> False
    assert book.get(loan_id)["returned_at"] == returned_at   # 시각이 덮어써지면 안 된다

    assert book.return_book(99) is False       # 없는 번호 -> False


def test_b2_return_book_changes_only_that_row(tmp_path):
    book = LoanBook(tmp_path / "loans.db")
    a = book.borrow("파이썬", "민수")
    b = book.borrow("SQL", "지수")

    book.return_book(a)

    assert book.get(b)["returned_at"] is None  # 다른 줄은 그대로 (WHERE 빠뜨리면 여기서 걸림)


def test_b2_not_returned_oldest_first(tmp_path):
    book = LoanBook(tmp_path / "loans.db")
    a = book.borrow("파이썬", "민수")
    b = book.borrow("SQL", "지수")
    c = book.borrow("리눅스", "민수")
    book.return_book(b)

    rows = book.not_returned()

    ids = []
    for row in rows:
        ids.append(row["id"])

    assert ids == [a, c]
    assert type(rows[0]) is dict


def test_b2_not_returned_empty(tmp_path):
    book = LoanBook(tmp_path / "loans.db")
    assert book.not_returned() == []


def test_b2_latest(tmp_path):
    book = LoanBook(tmp_path / "loans.db")
    for title in ["A", "B", "C", "D", "E"]:
        book.borrow(title, "민수")

    titles = []
    for row in book.latest():
        titles.append(row["title"])
    assert titles == ["E", "D", "C"]           # 기본 3개, 최신순

    titles = []
    for row in book.latest(limit=2):
        titles.append(row["title"])
    assert titles == ["E", "D"]


# -- B3. 안전한 검색과 시간 계산 --

@pytest.fixture
def sample_conn(tmp_path):
    """채점용: README의 loans 표와 같은 내용을 가진 연결"""
    with open_db(tmp_path / "s.db") as conn:
        create_table(conn)
        insert_sample(conn, "파이썬", "민수", "2026-11-01")
        insert_sample(conn, "SQL", "지수")
        insert_sample(conn, "리눅스", "민수")
        insert_sample(conn, "깃", "하늘", "2026-11-03")
        insert_sample(conn, "도커", "지수")
        yield conn


def test_b3_find_by_borrower(sample_conn):
    assert find_by_borrower(sample_conn, "민수") == ["파이썬", "리눅스"]
    assert find_by_borrower(sample_conn, "지수") == ["SQL", "도커"]
    assert find_by_borrower(sample_conn, "없는사람") == []


def test_b3_find_by_borrower_blocks_injection(sample_conn):
    # f-string 버전이면 5권이 전부 나온다. ? 를 쓰면 '그런 이름'은 없으니 빈 리스트.
    assert find_by_borrower(sample_conn, "' OR '1'='1") == []


def test_b3_find_by_borrower_allows_quote_in_name(sample_conn):
    insert_sample(sample_conn, "책", "O'Brien")
    # f-string 버전이면 따옴표 때문에 문법 에러. ? 는 그냥 '글자'로 다룬다.
    assert find_by_borrower(sample_conn, "O'Brien") == ["책"]


@pytest.mark.parametrize(
    "start, end, expected",
    [
        ("2026-11-22T08:00:00+09:00", "2026-11-22T09:30:00+09:00", 1.5),
        ("2026-11-22T08:00:00+09:00", "2026-11-23T08:00:00+09:00", 24.0),
        ("2026-11-22T08:00:00+09:00", "2026-11-22T08:20:00+09:00", 0.3),
        ("2026-11-22T23:00:00+09:00", "2026-11-22T23:00:00+09:00", 0.0),
    ],
)
def test_b3_hours_between(start, end, expected):
    assert hours_between(start, end) == expected
