# 시험 3회차 답안지

## A1
- (1) x.on: False
- (1) y.on: True
- (2): Lamp.switch(y)
- (3) 에러: AttributeError
- (3) 이유: self.on = False는 매개변수 on을 가리키는 것이고, on = False는 함수 내 지역변수를 가리키는 것이기때문임.

## A2
- (1): PASSED
- (2): FAILED
- (3): FAILED

## A3
- (1): CalendarError
- (2): ValueError가 일어난 에러내용
- (3): 무슨 에러가 생겼는지 __cause__을 보면 알 수 있다.

## A4
- 출력:
A 1
B

## A5
- (1): id가 login_btn인 것
- (2): class가 todo_title인 것
- (3): span태그 중에 class가 todo_d_day인 것
- (4): class가 span 이면서 '동시에' todo_d_day인 요소하나
- (5): div태그 중 class가 todo_date이고 그 바로 안 span태그 중 class가 todo_date인 것

## A6
- 좋은 점 1: 서비스를 한 번만 만들어 여러 번 재사용 가능
- 좋은 점 2: 테스트 중 실제 캘린더에 테스트 일정이 쌓이는 것을 방지

## A7
- (1) `??`: 새 파일
- (1) ` M`: 수정했지만 아직 add 안함
- (1) `M `: 수정하고 add까지 함 (커밋 대기)
- (2): git commit --amend -m "새 메세지"
