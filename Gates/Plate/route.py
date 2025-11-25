from fastapi import FastAPI
import asyncio

app = FastAPI()

# 서버 정상작동 여부를 판단하는 동기 요청 처리
@app.get("/door/healthy")
def is_healthy():
    return {"status": "Service is running"}


# 공장 문 개방 비동기 처리
@app.get("/door/open")
async def open():
    
    # 실제 DB 조회나 외부 API 호출과 같은 I/O 작업 시뮬레이션
    # asyncio.sleep은 비동기적으로 작동하여, 이 대기 시간 동안 서버는 다른 요청을 처리할 수 있습니다.
    await asyncio.sleep(1)
    return {"message": f"Opening the door..."}


# 공장 문 닫힘 비동기 처리
@app.get("/door/close")
async def close():
    await asyncio.sleep(1)
    return {"message": f"Closing the door..."}