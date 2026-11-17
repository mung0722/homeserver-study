"""
시험 3회차 자동 채점기 - 수정 금지!

새로 나오는 문법:
    isinstance(값, 클래스)
        -> 값이 그 클래스로 만든 객체(또는 그 자식 클래스의 객체)면 True
    issubclass(클래스A, 클래스B)
        -> 클래스A가 클래스B를 상속받았으면 True
    a is b
        -> a와 b가 '똑같은 하나의 객체'면 True (값이 같은지(==)가 아니라 같은 물건인지)
"""
import pytest

from q1_classes import StampCard
from q2_fakes import FakeClient, FakeMessages, FakeRequest
from q3_notify import NotifyError, send_all


# -- B1. 도장 카드 --

def test_b1_init_defaults():
    card = StampCard("민수")
    assert card.owner == "민수"
    assert card.goal == 10        # goal을 안 넘기면 기본값 10
    assert card.stamps == 0


def test_b1_custom_goal():
    assert StampCard("지수", goal=3).goal == 3


def test_b1_stamp_returns_whether_goal_reached():
    card = StampCard("민수", goal=3)
    assert card.stamp() is False      # 1개
    assert card.stamp(1) is False     # 2개
    assert card.stamp() is True       # 3개 = goal -> True ('이상'이므로 같아도 True)
    assert card.stamps == 3
    assert card.stamp(2) is True      # 5개 > goal -> 여전히 True
    assert card.stamps == 5


@pytest.mark.parametrize("bad", [0, -1])
def test_b1_bad_n_raises_and_keeps_stamps(bad):
    card = StampCard("민수")
    card.stamp(2)
    with pytest.raises(ValueError):
        card.stamp(bad)
    assert card.stamps == 2           # 에러가 나도 도장 수는 그대로여야 한다


def test_b1_reset():
    card = StampCard("민수", goal=3)
    card.stamp(3)
    card.reset()
    assert card.stamps == 0
    assert card.stamp() is False      # 리셋 뒤에는 처음부터 다시


def test_b1_cards_are_independent():
    a = StampCard("민수")
    b = StampCard("지수")
    a.stamp(4)
    assert a.stamps == 4
    assert b.stamps == 0              # a에 찍은 도장이 b에 들어가면 안 된다


# -- B2. 가짜 메신저 --

def test_b2_fake_request_returns_result():
    assert FakeRequest({"a": 1}).execute() == {"a": 1}


def test_b2_fake_messages_init():
    m = FakeMessages(["안녕", "안녕", "잘가"])
    assert m.existing_texts == {"안녕", "잘가"}   # set으로 저장 -> 중복이 사라짐
    assert m.sent == []


def test_b2_find():
    m = FakeMessages(["안녕"])
    assert m.find(channelId="c1", text="안녕").execute() == {"found": True}
    assert m.find(channelId="c1", text="잘가").execute() == {"found": False}
    # 이름 붙은 인자가 더 와도 받아 줘야 한다 (**kwargs)
    assert m.find(channelId="c1", text="안녕", limit=10).execute() == {"found": True}


def test_b2_send_records_body():
    m = FakeMessages([])
    result = m.send(channelId="c1", body={"text": "하나"}).execute()
    m.send(channelId="c1", body={"text": "둘"})
    assert result == {"id": "fake"}
    assert m.sent == [{"text": "하나"}, {"text": "둘"}]   # 보낸 순서대로 기록


def test_b2_client_returns_same_messages_object():
    client = FakeClient(["안녕"])
    first = client.messages()
    assert isinstance(first, FakeMessages)
    assert client.messages() is first             # 몇 번 불러도 '같은' 객체
    assert first.existing_texts == {"안녕"}


def test_b2_client_default_is_empty():
    client = FakeClient()
    assert client.messages().existing_texts == set()


# -- B3. 알림 보내기 --

def test_b3_notify_error_is_exception():
    assert issubclass(NotifyError, Exception)


def test_b3_sends_only_new_messages():
    client = FakeClient(["안녕"])
    assert send_all(["안녕", "잘가"], "c1", client) == (1, 1)
    assert client.messages().sent == [{"text": "잘가"}]


def test_b3_nothing_to_send_when_all_exist():
    client = FakeClient(["안녕", "잘가"])
    assert send_all(["안녕", "잘가"], "c1", client) == (0, 2)
    assert client.messages().sent == []


def test_b3_empty_list():
    assert send_all([], "c1", FakeClient()) == (0, 0)


def test_b3_error_in_messages_becomes_notify_error():
    class BrokenClient:
        def messages(self):
            raise RuntimeError("down")

    with pytest.raises(NotifyError) as error:
        send_all(["안녕"], "c1", BrokenClient())

    assert str(error.value) == "RuntimeError: down"
    assert isinstance(error.value.__cause__, RuntimeError)


def test_b3_error_in_send_becomes_notify_error():
    class SendFails(FakeMessages):        # FakeMessages를 상속받아 send만 고장 낸 가짜
        def send(self, channelId, body):
            raise ConnectionError("lost")

    class HalfBrokenClient:
        def __init__(self):
            self._messages = SendFails([])

        def messages(self):
            return self._messages

    with pytest.raises(NotifyError) as error:
        send_all(["안녕"], "c1", HalfBrokenClient())

    assert str(error.value) == "ConnectionError: lost"
    assert isinstance(error.value.__cause__, ConnectionError)
