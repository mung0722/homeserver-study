# 시험 2회차 답안지

## A1
- (1) %m: 몇월
- (1) %M: 몇분
- (2) 차이: %I는 12시간제, %H는 24시간제
- (2) %p의 짝: %I
- (3) 형식 문자열: %d/%m/%Y %H:%M

## A2
- (1) 출력:2026-11-07T23:59:00
- (2) 문제: 어느 나라의 시간인지 명시가 되어있지 않음
- (3) 해결: d.replace(tzinfo=KST)

## A3
- (1) 치우기: git stash
- (1) 꺼내기: git stash pop
- (2): git switch -c retry-02 exam-02-blank
- (3): git add 빠뜨린파일 && git commit --amend --no-edit
- (4): amend가 커밋의 번호를 바꿔버려서 충돌이 생김

## A4
- (1) 위쪽: 지금 커밋
- (1) 아래쪽: 서랍에 들어있던 내 수정
- (2): git add 파일
- (3) 남은 것: 꺼낸 그 stash 항목
- (3) 비우는 법: git stash drop

## A5
- (1): O
- (2): X
- (3): O
- (4): X