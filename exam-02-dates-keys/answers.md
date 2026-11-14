# 시험 2회차 답안지

## A1
- (1) %m: 몇월
- (1) %M: 몇분
- (2) 차이: %I는 12시간제, %H는 24시간제
- (2) %p의 짝: %I
- (3) 형식 문자열: %d/%m/%Y %H:%M

## A2
- (1) 출력: 2026-11-07T23:59:00
- (2) 문제: 시간대 정보가 없어서 어느 나라의 23:59인지 알 수 없음
- (3) 해결: d.replace(tzinfo=KST)로 시간대를 붙인다

## A3
- (1) 치우기: git stash
- (1) 꺼내기: git stash pop
- (2): git switch -c retry-02 exam-02-blank
- (3): git add 빠뜨린파일 && git commit --amend --no-edit
- (4): amend가 커밋번호를 바꿔서 Github에 있는 기록과 내 기록이 서로 달라지기때문, 억지로 하려면 force push가 필요함

## A4
- (1) 위쪽: 지금 커밋
- (1) 아래쪽: 서랍에서 꺼낸 내 수정
- (2): git add 파일
- (3) 남은 것: 꺼낸 그 stash 항목이 그대로 남아 있음
- (3) 비우는 법: git -stash drop

## A5
- (1): O
- (2): X
- (3): O
- (4): X