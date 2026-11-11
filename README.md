
# 공부용 시험 폴더

각 `exam-NN-주제/` 폴더가 시험 1회다. (Task가 하나 끝날 때마다 1회)

## 푸는 순서
1. `README.md`(문제지)를 읽는다.
2. 개념 문제(Part A) -> `answers.md`에 답을 적는다.
3. 코딩 문제(Part B) -> `q*.py`의 `# TODO` 자리를 채운다.
4. 스스로 채점한다 (몇 번이든 다시 실행해도 된다.)
    ```bash
    source ~/homeserver/lms-api/.venv/bin/activate
    cd ~/homeserver/study/exam-NN-주제
    pytest -v
    ```
5. Claude에게 "채점해 줘" -> 코드와 answers.md를 직접 읽고 채점· 해설

## 규칙
- `test_grading.py`(채점기)는 수정하지 않는다. (고쳐서 통과시키면 반칙!)
- 모르면 비워 두고 질문한다. 틀려도 괜찮다. 틀린 걸 아는게 공부다.