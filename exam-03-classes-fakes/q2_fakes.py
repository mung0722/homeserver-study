"""
B2. 가짜 메신저 - lms-api/tests/test_calendar_sync.py의 FakeRequest/FakeEvents/FakeService 응용

규칙은 문제지(README.md) B2 참고
"""


class FakeRequest:
    def __init__(self, result):
        # TODO 1: 나중에 돌려줄 result를 기억해 둔다.
        self.result = result
        # pass  # 코드 작성 후 삭제

    def execute(self):
        # TODO 2: 기억해 둔 result를 그대로 돌려준다.
        return self.result
        # pass  # 코드 작성 후 삭제


class FakeMessages:
    def __init__(self, existing_texts):
        # TODO 3: existing_texts를 set으로 바꿔서 저장한다.
        self.existing_texts = set(existing_texts)

        # TODO 4: 보낸 body를 기록할 빈 리스트 sent를 만든다.
        self.sent = []
        # pass  # 코드 작성 후 삭제

    def find(self, channelId, text, **kwargs):
        # TODO 5: text가 existing_texts에 있으면 {"found": True},
        #         없으면 {"found": False}를 맡긴 FakeRequest를 돌려준다.
        if text in self.existing_texts:
            return FakeRequest({"found": True})
        else:
            return  FakeRequest({"found": False})

        # pass  # 코드 작성 후 삭제

    def send(self, channelId, body):
        # TODO 6: body를 sent에 기록하고, {"id": "fake"}를 맡긴 FakeRequest를 돌려준다.
        self.sent.append(body)
        return FakeRequest({"id":"fake"})

        # pass  # 코드 작성 후 삭제



class FakeClient:
    def __init__(self, existing_texts=()):
        # TODO 7: FakeMessages 객체를 '한 번만' 만들어 속성 _messages에 보관한다.
        self._messages = FakeMessages(set(existing_texts))
        # pass  # 코드 작성 후 삭제

    def messages(self):
        # TODO 8: 보관해 둔 그 객체를 돌려준다. (매번 새로 만들면 안 된다!)
        return self._messages
        # pass  # 코드 작성 후 삭제
