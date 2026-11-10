"""
B2. 설정 검사기 - app/config.py 응용

규칙은 문제지(README.md) B2 참고
"""
from collections.abc import Mapping
from dataclasses import dataclass, field

REQUIRED = ["STUDY_NAME", "STUDY_PORT", "STUDY_TOKEN"]

# TODO 1: StudyError 클래스 (Exception 상속)
# TODO 2: StudyConfigError 클래스 (StudyError 상속)
# TODO 3: StudyConfig - frozen dataclass
#           필드: name(str), port(int), token(str, repr에서 숨김)

def load_study_config(env: Mapping[str,str]) -> "StudyConfig":
    # (반환 타입에 따옴표를 친 이유: 처음엔 StudyConfig가 아직 없으니
    # "나중에 정의될 이름"이라고 문자열로 적어 둔 것)

    # TODO 4: 규칙 1. 빠진 값 검사
    # TODO 5: 규칙 2. 포트가 숫자인지 검사
    # TODO 6: 규칙 3. 포트 범위 검사 (int로 바꾼 뒤 비교)
    # TODO 7: 규칙 4. 토큰 길이 검사
    # TODO 8: 규칙 5. StudyConfig를 만들어 돌려줌 (port는 int!)
    pass
