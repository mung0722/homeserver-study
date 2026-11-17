"""
B3. 알림 보내기 - lms-api/app/calendar_sync.py의 sync_calendar 응용

규칙은 문제지(README.md) B3 참고
"""


# TODO 1: NotifyError 클래스 (Exception 상속)
class NotifyError:
    pass


def send_all(messages: list[str], channel_id: str, client) -> tuple[int, int]:
    # TODO 2: sent, skipped를 0으로 시작한다.

    # TODO 3: 아래 전체를 try로 감싼다.
    #   for 글자 in messages:
    #       - client.messages().find(channelId=..., text=...).execute()로 이미 보냈는지 확인
    #       - 결과의 "found"가 True면 skipped += 1 하고 다음 글자로 (힌트: continue)
    #       - 아니면 client.messages().send(channelId=..., body={"text": ...}).execute()
    #         하고 sent += 1

    # TODO 4: 어떤 에러든(Exception) 잡아서 NotifyError로 바꿔 던진다.
    #   메시지: "원래에러이름: 원래메시지"  (힌트: type(error).__name__)
    #   원래 에러를 원인으로 연결한다. (힌트: from)

    # TODO 5: (sent, skipped)를 돌려준다.
    pass  # 코드 작성 후 삭제
