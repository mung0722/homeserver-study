"""
B2. 키 만들기와 중복 제거 - app/calendar_sync.py의 create_assignment_key 응용

규칙은 문제지(README.md) B2 참고
"""
import hashlib


def make_key(item: dict, fields: list[str]) -> str:
    # TODO 1: fields 순서대로 item의 값을 꺼내 "|"로 이어 붙인다.
    #       (힌트: 리스트 컴프리헨션 + "|".join)
    raw_key = "|".join([item[name] for name in fields])

    # TODO 2: SHA-256 16진수 문자열로 바꿔서 돌려준다.
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    # pass # 코드 작성 후 삭제 or 주석처리하여 없애기

# list[dict], set[str]같은 것들은 함수가 무엇을 받는지를 알려주는 타입힌트임
def find_new(items: list[dict], existing: set[str], fields: list[str]) -> list[dict]:
    # TODO 3: existing을 '복사'한 set을 만듦 (원본은 절대 건드리지 않기)
    #           파이썬에서 =는 복사하는 것이 아닌 같은 물건에 이름표를 하나 더 붙일 뿐임.
    seen = set(existing)

    # TODO 4: 결과를 담을 빈 리스트를 만든다.
    result = []

    # TODO 5: items를 하나씩 돌면서
    #       - 키를 만들고
    #       - 이미 본 키면 건너뛰고 (힌트: continue)
    #       - 처음 본 키면 '본 키 목록'에 추가하고, 결과 리스트에도 추가
    for item in items:
        key = make_key(item, fields) # 이 과제의 지문을 만들고
        if key in seen: # 이미 본 지문이면 (이미 등록됐거나, 이번 목록에서 앞에 나왔거나)
            continue

        seen.add(key) # 처음 본 지문이면 '본 목록'에서 기록하고 (복사만에만)
        result.append(item) # 결과에 추가

    # TODO 6: 결과 리스트를 돌려줌
    return result
    # pass # 코드 작성 후 삭제 or 주석처리하여 없애기