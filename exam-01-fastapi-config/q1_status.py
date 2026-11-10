"""
B1. 나만의 작은 API

조건 (문제지 참고):
    - title = "Study API"
    - GET /ping -> {"pong": True}
    - GET /about -> {"service": "study", "version": "0.1.0"}
"""

from fastapi import FastAPI

def create_app() -> FastAPI:
    # TODO 1: 제목이 "Study API"인 FastAPI앱을 만듦
    # TODO 2: GET /ping 메뉴를 등록
    # TODO 3: GET /about 메뉴를 등록함
    # TODO 4: 앱을 돌려줌

    pass # <- 다 작성하면 이 줄은 지운다 (pass = "아무것도 안함" 자리 채우기용)