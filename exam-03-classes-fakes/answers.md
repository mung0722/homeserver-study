# 시험 3회차 답안지

## A1
- (1) x.on: False
- (1) y.on: True
- (2): Lamp.switch(y)
- (3) 에러: 속성에러
- (3) 이유: self.on = false는 속성이고, on = false는 변수이기때문에 on = false를 사용하면 x.switch()에는 비어있기때문에 속성에러가 나옴

## A2
- (1): PASSED
- (2): FAILED
- (3): FAILED

## A3
- (1): CalendarError
- (2): 무슨 에러인지
- (3): __cause__로 에러가 입력되어 추후 __cause__를 확인하여 어떤 에러인지 구체적으로 확인하여 고치기 수월하다

## A4
- 출력:A 1
B

## A5
- (1): id가 login_btn인 요소
- (2): class가 todo_title인 요소
- (3): class가 todo_d_day인 span 요소
- (4): class가 span이면서 todo_d_day인 요소
- (5): class가 todo_date 인 div 요소 바로 안에 있는 class가 todo_date인 span 요소

## A6
- 좋은 점 1: 서비스를 한개만 만들 수 있다.
- 좋은 점 2: 테스트를 할 때 용이하다.

## A7
- (1) `??`: 새로운 파일
- (1) ` M`: 수정한 파일
- (1) `M `: add한 수정 파일
- (2):git --amend commit -m "메시지"
