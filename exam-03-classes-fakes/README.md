# 시험 3회차 - 클래스, 가짜 객체, 에러 감싸기
범위: Task 3 (`sync_calendar`, `google_auth`, `scraper` 옮기기) + 클래스 기초

채점: `cd ~/homeserver/study/exam-03-classes-fakes && python -m pytest test_grading.py -v`

---

## Part A. 개념 문제 -> `answers.md`에 작성

**A1. 클래스 읽기**

```python
class Lamp:
    def __init__(self, color):
        self.color = color
        self.on = False

    def switch(self):
        self.on = not self.on
        return self.on

x = Lamp("노랑")
y = Lamp("파랑")
x.switch()
x.switch()
y.switch()
```

- (1) 마지막 줄까지 실행한 뒤 `x.on`과 `y.on`의 값은?
- (2) `y.switch()`를 파이썬이 속으로 바꿔 실행하는 모양을 `Lamp.switch(...)` 형태로 쓰시오.
- (3) `__init__` 안의 `self.on = False`를 `on = False`로 바꾸면 `x.switch()`에서 어떤 에러가 나는가? 왜 그런가?

**A2. pytest.raises**

```python
with pytest.raises(KeyError):
    f()
```

`f()`가 각각 아래처럼 동작할 때 테스트 결과(PASSED/FAILED)를 쓰시오.
- (1) `KeyError`를 낸다.
- (2) 아무 에러 없이 끝난다.
- (3) `ValueError`를 낸다.

**A3. raise ... from**

```python
try:
    int("abc")
except ValueError as error:
    raise CalendarError("변환 실패") from error
```

- (1) 위 코드가 바깥으로 던지는 에러의 종류는?
- (2) 그 에러 객체의 `__cause__`에는 무엇이 들어 있는가?
- (3) `from error`를 붙이면 디버깅할 때 무엇이 좋은가?

**A4. 들여쓰기와 break**

```python
for n in [1, 2, 3]:
    if n == 2:
        break
    print("A", n)
print("B")
```

출력 결과를 순서대로 모두 쓰시오.

**A5. CSS 선택자** - 각각 무엇을 찾는지 쓰시오.
- (1) `#login_btn`
- (2) `.todo_title`
- (3) `span.todo_d_day`
- (4) `.span.todo_d_day`
- (5) `div.todo_date > span.todo_date`

**A6. 의존성 주입**

`sync_calendar(assignments, calendar_id, service)`처럼 `service`를 함수 안에서 만들지 않고 **인자로 받으면** 좋은 점을 두 가지 쓰시오.

**A7. Git**
- (1) `git status --short`에서 `??`, ` M`(앞이 빈칸), `M `(뒤가 빈칸)는 각각 무슨 뜻인가?
- (2) 방금 한 커밋(아직 push 안 함)의 **메시지만** 고치는 명령은?

---

## Part B. 코딩 문제 -> `q*.py`의 `# TODO` 채우기

### B1. `q1_classes.py` - 도장 카드

`StampCard` 클래스를 만든다.
1. `StampCard(owner, goal=10)`
    - 속성 `owner`, `goal`을 저장하고, 속성 `stamps`는 `0`에서 시작한다.
2. `stamp(n=1)`
    - 도장을 `n`개 찍는다. (`stamps`에 `n`을 더한다)
    - `n`이 0 이하면 `ValueError`를 던지고, 도장 수는 **바뀌면 안 된다.**
    - 찍은 뒤 `stamps`가 `goal` **이상**이면 `True`, 아니면 `False`를 돌려준다.
3. `reset()`
    - `stamps`를 `0`으로 되돌린다.

카드 두 장은 서로 **영향을 주면 안 된다.**

### B2. `q2_fakes.py` - 가짜 메신저 만들기

진짜 메신저 클라이언트는 이렇게 쓴다.

```python
client.messages().find(channelId="c1", text="안녕").execute()          # -> {"found": True 또는 False}
client.messages().send(channelId="c1", body={"text": "안녕"}).execute() # -> {"id": "..."}
```

인터넷 없이 테스트할 수 있도록 **모양이 똑같은 가짜**를 만든다.
1. `FakeRequest(result)`: `execute()`하면 맡겨 둔 `result`를 그대로 돌려준다.
2. `FakeMessages(existing_texts)`
    - 속성 `existing_texts`: 이미 보낸 것으로 칠 글자들 (`set`으로 저장)
    - 속성 `sent`: `send`로 받은 `body`를 차례대로 기록하는 리스트 (처음엔 비어 있음)
    - `find(channelId, text, **kwargs)`: `text`가 `existing_texts`에 있으면 `{"found": True}`, 없으면 `{"found": False}`를 맡긴 `FakeRequest`를 돌려준다.
    - `send(channelId, body)`: `body`를 `sent`에 기록하고, `{"id": "fake"}`를 맡긴 `FakeRequest`를 돌려준다.
3. `FakeClient(existing_texts=())`
    - `messages()`를 **몇 번 불러도 같은** `FakeMessages` 객체를 돌려준다.

### B3. `q3_notify.py` - 알림 보내기 (`sync_calendar` 응용)

1. 예외 클래스 `NotifyError` (Exception 상속)
2. `send_all(messages, channel_id, client)`
    - `messages`: 보낼 글자 리스트
    - 글자마다 `find`로 이미 보냈는지 확인한다. 이미 보냈으면 건너뛰고 `skipped`를 1 늘린다.
    - 아니면 `send`로 `body={"text": 글자}`를 보내고 `sent`를 1 늘린다.
    - `(sent, skipped)` 튜플을 돌려준다.
    - 도중에 **어떤 에러든** 나면 `NotifyError`로 **바꿔서** 던진다.
        - 메시지는 `"원래에러이름: 원래메시지"` 모양 (예: `"RuntimeError: down"`)
        - 원래 에러를 **원인(cause)으로 연결**한다.

> 새 도구 / 다시 보기
> - `not 값` -> `True`는 `False`로, `False`는 `True`로 뒤집는다.
> - `type(error).__name__` -> 에러 클래스의 이름 글자 (예: `"RuntimeError"`)
> - `**kwargs` -> 이름 붙은 인자를 몇 개든 받아 두는 자리 (안 써도 됨)
> - 채점기는 **여러분이 B2에서 만든 가짜**로 B3을 검사한다. B2가 틀리면 B3도 같이 틀릴 수 있다.
