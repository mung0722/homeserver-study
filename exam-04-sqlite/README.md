# 시험 4회차 - SQLite, with, 실행 기록 저장소
범위: Task 4 (`app/runs_db.py`의 `RunStore`) + SQL 기본 문법

채점:

```bash
source ~/homeserver/lms-api/.venv/bin/activate
```

```bash
cd ~/homeserver/study/exam-04-sqlite
```

```bash
pytest -v
```

---

## 문제에서 쓰는 `loans`(도서 대출) 표

Part A의 SQL 문제는 모두 **아래 상태의 표**를 기준으로 한다.

| id | title | borrower | returned_at |
|---|---|---|---|
| 1 | 파이썬 | 민수 | 2026-11-01 |
| 2 | SQL | 지수 | NULL |
| 3 | 리눅스 | 민수 | NULL |
| 4 | 깃 | 하늘 | 2026-11-03 |
| 5 | 도커 | 지수 | NULL |

- `returned_at`이 `NULL` = 아직 반납 안 함

---

## Part A. 개념 문제 -> `answers.md`에 작성

**A1. SELECT 결과 예측**

각 SQL의 결과를 **순서대로** 쓰시오. (힌트: FROM -> WHERE -> ORDER BY -> LIMIT 순서로 끝까지 따라가기)

```sql
-- (1)
SELECT id
FROM loans
WHERE returned_at IS NULL
ORDER BY id DESC
```

```sql
-- (2)
SELECT id
FROM loans
WHERE borrower IN ('민수', '하늘')
ORDER BY id DESC
LIMIT 2
```

```sql
-- (3)
SELECT title
FROM loans
WHERE id NOT IN (
    SELECT id
    FROM loans
    ORDER BY id DESC
    LIMIT 3
)
```

- (4) **직접 쓰기**: "지수가 빌린 책 중 **아직 반납 안 한** 것의 `title`을 최신순(id 큰 것부터)으로" 가져오는 SQL을 쓰시오.
    - 새 문법 `AND`: `WHERE 조건1 AND 조건2` -> 두 조건이 **모두** 참인 줄만
    - 한 줄에 한 절씩 (한줄코딩 금지)

**A2. UPDATE / DELETE와 rowcount**

각 SQL을 (원래 표에서) 실행한 직후 `cursor.rowcount`는 몇인가?

```sql
-- (1)
UPDATE loans
SET returned_at = '2026-11-22'
WHERE borrower = '민수'
```

```sql
-- (2)
DELETE FROM loans
WHERE id = 99
```

```sql
-- (3)
UPDATE loans
SET returned_at = '2026-11-22'
WHERE borrower = '민수'
  AND returned_at IS NULL
```

- (4) (1)과 (3) 중 "민수가 **아직 안 돌려준 책**을 반납 처리"하려는 의도에 맞는 것은? 다른 하나는 무엇이 문제인가?

**A3. 튜플과 쉼표**

```python
conn.execute(
    """
    SELECT *
    FROM loans
    WHERE borrower = ?
    """,
    ("지수"),
)
```

- (1) 이 코드는 에러가 난다. 파이썬은 `("지수")`를 **무엇**으로 보는가?
- (2) `execute`는 두 번째 재료를 어떻게 쓰기 때문에, 이 경우 "? 는 1개인데 값이 2개"라는 에러가 나는가?
- (3) 고친 한 줄을 쓰시오.

**A4. `with conn`과 rollback**

`_connect`는 `RunStore._connect`와 똑같이 만들어져 있다.

```python
with self._connect() as conn:
    conn.execute(
        """
        INSERT INTO loans (title, borrower)
        VALUES (?, ?)
        """,
        ("네트워크", "하늘"),
    )
    conn.execute(
        """
        UPDATE loans
        SET retuned_at = '2026-11-22'
        WHERE id = 6
        """
    )
```

- (1) 두 번째 `execute`에서 에러가 난다. 무슨 에러이고 원인은 무엇인가?
- (2) 이 코드가 끝난 뒤 `네트워크` 책 줄은 표에 **남아 있는가**? 이유는?
- (3) 에러가 났는데도 연결이 닫히는 것은 `_connect`의 **어느 부분** 덕분인가?

**A5. SQL 인젝션**

```python
name = input("이름: ")
sql = f"SELECT * FROM loans WHERE borrower = '{name}'"
```

- (1) 사용자가 `' OR '1'='1` 을 입력했다. 완성된 `sql` 글자를 그대로 쓰시오.
- (2) 그 SQL은 위 표에서 몇 줄을 돌려주는가? 왜 그런가?
- (3) `?`를 쓰면 왜 안전해지는가? 한두 문장으로.

**A6. `@contextmanager` 실행 순서**

```python
from contextlib import contextmanager

@contextmanager
def box():
    print("1 열기")
    try:
        yield "선물"
    finally:
        print("3 닫기")

with box() as x:
    print("2", x)
print("4 끝")
```

- (1) 출력 결과를 순서대로 모두 쓰시오.
- (2) `with` 블록 안 `print("2", x)` 다음 줄에 `raise ValueError("앗")`을 추가했다. 이제 출력되는 줄을 모두 쓰고, 마지막에 무슨 일이 일어나는지 쓰시오.
- (3) `yield` 와 `finally` 는 각각 어떤 역할인가?

**A7. 시간 계산**

```python
from datetime import datetime

started = datetime.fromisoformat("2026-11-22T08:00:00+09:00")
finished = datetime.fromisoformat("2026-11-22T08:01:02.46+09:00")
elapsed = finished - started
```

- (1) `elapsed.total_seconds()`의 값은?
- (2) `round(elapsed.total_seconds(), 1)`의 값은?
- (3) `RunStore`는 시각을 DB에 **글자(`isoformat()`)** 로 저장한다. 꺼낼 때 `datetime.fromisoformat(...)`으로 다시 바꾸는 이유는?

**A8. Git**
- (1) 새로 만든 파일을 `git add` 한 직후, `git status --short`에서 그 파일 앞에는 무엇이 보이는가?
- (2) `?? app/x.py` 상태에서 바로 `git commit -m "..."`을 하면 `app/x.py`는 커밋에 들어가는가?

---

## Part B. 코딩 문제 -> `q*.py`의 `# TODO` 채우기

> 모든 코드는 **한줄코딩 금지**: SQL은 한 줄에 한 절/한 열, 긴 호출은 인자 한 줄에 하나.

### B1. `q1_connect.py` - 연결 도우미와 표 만들기

1. `CREATE_TABLE_SQL`: 아래 열을 가진 `loans` 표를 만드는 SQL (이미 있으면 넘어가기)

    | 열 | 타입 / 조건 |
    |---|---|
    | `id` | 정수, 기본 키, 자동 증가 |
    | `title` | 글자, 비어 있으면 안 됨 |
    | `borrower` | 글자, 비어 있으면 안 됨 |
    | `borrowed_at` | 글자, 비어 있으면 안 됨 |
    | `returned_at` | 글자 (비어 있어도 됨) |

2. `open_db(path)`: `with open_db(path) as conn:`으로 쓰는 연결 도우미 (`RunStore._connect`와 같은 동작)
    - 연결을 열고, 행을 `row["title"]`처럼 열 이름으로 읽을 수 있게 설정한다.
    - 블록이 무사히 끝나면 commit, 에러가 나면 rollback
    - 어느 쪽이든 마지막에 **반드시** 연결을 닫는다.
3. `create_table(conn)`: 받은 연결로 `CREATE_TABLE_SQL`을 실행한다.

### B2. `q2_loans.py` - 대출 장부 `LoanBook`

`RunStore`처럼 **메서드마다 `open_db`로 연결을 새로 열고 닫는다.**

1. `LoanBook(db_path)`
    - 속성 `db_path`에 `Path`로 저장한다.
    - DB 파일이 들어갈 폴더가 없으면 (중간 폴더까지) 만든다.
    - 표를 만든다. (`create_table` 사용)
2. `borrow(title, borrower) -> int`
    - `borrowed_at`은 `now_kst().isoformat()`, `returned_at`은 비워 둔 채로 한 줄 추가
    - 새 줄의 `id`를 돌려준다. (`None`이면 `RuntimeError`)
3. `get(loan_id) -> dict | None`
    - 그 번호의 줄을 **진짜 딕셔너리**로. 없으면 `None`
4. `return_book(loan_id) -> bool`
    - 그 번호의 책이 **아직 반납 안 된 경우에만** `returned_at`을 지금 시각으로 채운다.
    - 실제로 반납 처리했으면 `True`, 없는 번호이거나 **이미 반납된 책**이면 `False`
5. `not_returned() -> list[dict]`
    - 반납 안 된 줄 전부를 **오래된 순**(id 작은 것부터)으로
6. `latest(limit=3) -> list[dict]`
    - 최근 줄을 **최신순**으로 최대 `limit`개

### B3. `q3_safe.py` - 안전한 검색과 시간 계산

1. `find_by_borrower(conn, name) -> list[str]`
    - 파일 안에 **위험한 버전**이 주석으로 있다. `?`를 써서 안전하게 다시 쓴다.
    - 그 사람이 빌린 책 `title`들을 id 순서(작은 것부터) 리스트로
2. `hours_between(start_iso, end_iso) -> float`
    - ISO 글자 두 개를 받아 그 사이가 **몇 시간**인지 소수 첫째 자리까지 반올림해 돌려준다.
    - 예: `"2026-11-22T08:00:00+09:00"` ~ `"2026-11-22T09:30:00+09:00"` -> `1.5`

> 새 도구 / 다시 보기
> - `WHERE 조건1 AND 조건2` -> 두 조건이 모두 참인 줄만
> - `cursor.rowcount` -> 방금 UPDATE/DELETE에 **걸린** 줄 수
> - `cursor.lastrowid` -> 방금 INSERT한 줄의 id (`int | None`)
> - `1시간 = 3600초`
> - 채점기는 B2·B3를 검사할 때 **여러분이 B1에서 만든** `open_db`/`create_table`을 쓴다. B1이 틀리면 뒤도 같이 틀릴 수 있다.
