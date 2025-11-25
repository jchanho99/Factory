from fastapi import FastAPI
import asyncio
import aio_pika
from config import settings
# from typing import Dict, Any


app = FastAPI()

# ----------------- 가상 서비스 (Mock Services) -----------------

# 1. 가상 DB 확인 함수
async def check_plate_in_db(plate_number: str) -> bool:
    """번호판이 등록된 차량인지 DB에서 비동기적으로 확인합니다."""
    # DB 조회 시뮬레이션을 위해 500ms 대기
    await asyncio.sleep(0.5) 
    
    # 예시: "12가3456" 번호판은 등록되어 있다고 가정
    registered_plates = {"12가3456", "99나8888"}
    
    return plate_number in registered_plates

# 2. 가상 RabbitMQ 전송 함수
async def publish_confirmation_to_mq(plate_number: str, is_confirmed: bool):
    """확인 결과를 RabbitMQ 큐에 비동기적으로 전송합니다."""
    
    connection = None
    try:
        # 비동기적으로 RabbitMQ 연결
        connection = await aio_pika.connect_robust(settings.rabbitmq_url)
        
        async with connection:
            # 채널 생성
            channel = await connection.channel()
            
            # 큐 선언 (큐가 없으면 생성, durable=True로 설정하여 서버 재시작에도 유지)
            queue = await channel.declare_queue(settings.rabbitmq_queue_name, durable=True)
            
            # 메시지 본문 생성
            message_body = {
                "plate_number": plate_number,
                "is_confirmed": is_confirmed,
                "timestamp": asyncio.time() # 전송 시각
            }
            
            # 메시지를 JSON 문자열로 변환하여 발행
            message = aio_pika.Message(
                body=str(message_body).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )
            
            await channel.default_exchange.publish(
                message,
                routing_key=settings.rabbitmq_queue_name,
            )
            print(f"✅ Published to MQ: {message_body}")
            
    except aio_pika.exceptions.AMQPConnectionError as e:
        print(f"RabbitMQ Connection Error: {e}")
        # RabbitMQ 연결 실패 시에도 API 호출은 성공으로 처리할 수 있습니다 (로깅 후 다음 단계 진행)
    except Exception as e:
        print(f"An unexpected error occurred during MQ publish: {e}")
    finally:
        # aio_pika.connect_robust는 연결을 자동으로 닫으므로 명시적인 close는 필요하지 않을 수 있습니다.
        pass


# ----------------- FastAPI 엔드포인트 -----------------

@app.get("/plate/check")
def is_env_loaded():
    return {"status": settings.is_env_ok}


@app.get("/plate/healthy")
def is_server_healthy():
    return {"status": "Service is running"}


@app.get("/plate/confirm")
async def confirm_license_plate(video_data: str = "camera_stream_data_placeholder"):
    """
    카메라 데이터를 처리하고 번호판을 확인한 후, 결과를 RabbitMQ에 전송합니다.
    """
    
    # 1. 동영상 데이터를 이용해 번호판 인식 및 판별 (AI 모델 시뮬레이션)
    # 실제로는 동영상 데이터를 처리하고 AI 모델을 실행하는 무거운 작업이 여기에 포함됩니다.
    await asyncio.sleep(1.0) # AI 모델 처리 시뮬레이션 (1초 대기)
    
    # AI 모델이 추출한 가상의 번호판 (예시)
    plate_extracted = "12가3456" 

    # 2. DB에 해당 번호판이 존재하는지 확인
    is_plate_registered = await check_plate_in_db(plate_extracted)
    
    # 3. DB에 존재할 경우 (True), RabbitMQ에 전송
    if is_plate_registered:
        print(f"➡️ Plate {plate_extracted} confirmed. Publishing result to MQ.")
        await publish_confirmation_to_mq(plate_extracted, True)
        
        return {
            "status": "Processing successful",
            "plate_number": plate_extracted,
            "is_registered": True,
            "message": "Confirmation sent to MQ."
        }
    else:
        print(f"➡️ Plate {plate_extracted} not found in DB.")
        
        return {
            "status": "Processing successful",
            "plate_number": plate_extracted,
            "is_registered": False,
            "message": "Plate not registered. No message sent to MQ."
        }