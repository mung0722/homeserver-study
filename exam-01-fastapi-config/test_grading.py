"""
시험 1회차 자동 채점기 — 수정 금지!

새로 나오는 문법:
  pytest.raises(예외, match="글자")
    → 예외가 발생해야 하고, 그 메시지 안에 "글자"가 들어 있어야 통과
  isinstance(값, 타입)
    → 값이 그 타입인지 확인. isinstance(8001, int) → True
"""
import pytest
from fastapi.testclient import TestClient

from q1_status import create_app
from q2_config import StudyConfigError, StudyError, load_study_config


# ────────────── B1 ──────────────

def test_b1_title():
    assert create_app().title == "Study API"


def test_b1_ping():
    response = TestClient(create_app()).get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_b1_about():
    response = TestClient(create_app()).get("/about")
    assert response.status_code == 200
    assert response.json() == {"service": "study", "version": "0.1.0"}


def test_b1_unknown_path_is_404():
    # 메뉴판에 없는 경로는 404여야 한다
    assert TestClient(create_app()).get("/pong").status_code == 404


# ────────────── B2 ──────────────

# 모든 규칙을 통과하는 정상 설정
GOOD = {"STUDY_NAME": "엔백이", "STUDY_PORT": "8001", "STUDY_TOKEN": "token-12345"}


def test_b2_error_family():
    assert issubclass(StudyConfigError, StudyError)
    assert issubclass(StudyError, Exception)


def test_b2_reads_and_converts_port():
    config = load_study_config(GOOD)
    assert config.name == "엔백이"
    assert config.port == 8001                 # 문자열 "8001"이 아니라 숫자 8001
    assert isinstance(config.port, int)


def test_b2_missing_names_are_all_listed():
    env = {"STUDY_PORT": ""}                    # NAME, TOKEN은 없음 / PORT는 빈 값
    with pytest.raises(StudyConfigError) as error:
        load_study_config(env)
    for name in REQUIRED_NAMES:
        assert name in str(error.value)


REQUIRED_NAMES = ["STUDY_NAME", "STUDY_PORT", "STUDY_TOKEN"]


@pytest.mark.parametrize("port", ["abc", "80a", "-1", "8 001"])
def test_b2_port_must_be_digits(port):
    with pytest.raises(StudyConfigError, match="STUDY_PORT"):
        load_study_config({**GOOD, "STUDY_PORT": port})


# 경계값 테스트: (입력 포트, 통과해야 하나?)
@pytest.mark.parametrize("port, allowed", [
    ("1023", False),
    ("1024", True),
    ("65535", True),
    ("65536", False),
])
def test_b2_port_range_boundaries(port, allowed):
    env = {**GOOD, "STUDY_PORT": port}
    if allowed:
        assert load_study_config(env).port == int(port)
    else:
        with pytest.raises(StudyConfigError, match="STUDY_PORT"):
            load_study_config(env)


def test_b2_short_token_is_rejected_without_leaking():
    with pytest.raises(StudyConfigError) as error:
        load_study_config({**GOOD, "STUDY_TOKEN": "abc1234"})   # 7자
    assert "STUDY_TOKEN" in str(error.value)
    assert "abc1234" not in str(error.value)


def test_b2_token_of_exactly_8_is_allowed():
    assert load_study_config({**GOOD, "STUDY_TOKEN": "12345678"}).token == "12345678"


def test_b2_token_hidden_in_repr():
    text = repr(load_study_config(GOOD))
    assert "엔백이" in text                     # 비밀이 아닌 값은 보이고
    assert "token-12345" not in text           # 토큰은 숨김


def test_b2_config_is_frozen():
    config = load_study_config(GOOD)
    with pytest.raises(AttributeError):
        config.port = 9000