# 시험 1회차 - FastAPI 기초 · 예외 · 설정 검사

범위 : Take1 (FastAPI `/health`) ~ Task 2-1 (`errors.py`, `config.py`)

---

## Part A. 개념 문제 -> `answers.md`에 작성

**A1.** 상황에 맞는 상태 코드를 고르시오. (`200`, `202`, `401`, `404`, `409`, `500`)
- (a) `GET /runs/999` - 999번 실행기록이 존재하지 않음
- (b) `POST /sync` - 정상 접수됨. 작업은 백드라운드에서 이제 막 시작함
- (c) `GET /health` - 정상
- (d) 우리 코드에서 처리하지 않은 `KeyError`가 발생함

**A2.** `uvicorn app.main:create_capp --factory --host 127.0.0.1 -- port 8001`로 실행했다.
- (1) 엔백이에서 `curl http://127.0.0.1:8001/health -> 될까? 이유는?
- (2) 맥 브라우저에서 `http://ymhn100server:8001/health -> 될까? 이유는?

**A3.** 아래 코드의 결과를 예측하시오.
```python
class AError(Exception): pass
class BError(AError): pass
class CError(BError): pass

print(issubclass(CError, AError)) # (1)
print(issubclass(AError, CError)) # (2)

try:
    raise CError("x")
except BError:
    print("B로 잡힘") # (3) 출력될까?
except AError:
    print("A로 잡힘") # (4) 출력될까?
```

**A4.** `.gitignore`에 아래처럼 적었더니 `.env`가 Git에서 무시되지 않았다.
이유는 무엇이고, 어떻게 고쳐야 하는가?

```gitignore
.env # 비밀번호 파일
```

**A5.** `@dataclass(frozen=True)`로 만든 설정 객체에서 `config.port = 9000`을 실행하면 어떻게 되는가? 그리고 **설정 객체**을 frozen으로 만드는게 왜 좋은가?

---

## Part B. 코딩 문제 -> `q*.py`의 `# TODO` 채우기

### B1. `q1_status.py` - 나만의 작은 API
`create_app()` 함수가 아래 조건을 만족하는 FastAPI 앱을 돌려주게 하시오.
- 앱 제목(title)은 `"Study API"`
- `GET /ping` -> `{"pong": true}` (파이썬에서는 `True`)
- `GET /about`-> `{"service": "study", "version": "0.1.0"}`

### B2. `q2_config.py` - 설정 검사기
`config.py`에서 배운 것을 응용한다.

1. 예외 클래스 2개: `StudyError`(Exception 상속), `studyConfigError`(StudyError 상속)
2. frozen dataclass `StudyConfig`: 필드 `name:str`, `port:int`, `token:stk`
    - `token`은 print/repr에 **보이지 않아야**한다.
3. `load_study_config(env)` 규칙 - 어기면 전부 `StudyConfigError`
    1. `STUDY_NAME`, `STUDY_PORT`, `STUDY_TOKEN`중 없거나 빈 것이 있으면 -> 빠진 **이름을 모두** 메시지에
    2. `STUDY_PORT`가 숫자가 아니면 -> 메시지에 `STUDY_PORT` 포함
    3. 포스가 `1024`보다 작거나 `65535`보다 크면 -> 메시지에 `STUDY_PORT` 포함 (1024와 65535는 **허용**)
    4. `STUDY_TOKEN`이 8자 미만이면 -> 메시지에 `STUDY_TOKEN` 포함, **토큰 값은 노출 금지**
    5. 통과하면 `port`는 **정수로 변환해서** 담아 돌려준다.
> 새 도구 2개
> - `"8001".isdigit()` -> `True`, `"80a".isdigit()` -> `False`, `"-1".isdigit()` -> `False` (숫자로만 이루어졌나?)
> - `int("8001")` -> `8001` (문자열을 정수로 변환. 환경변수는 항상 **문사열**로 들어온다!)

