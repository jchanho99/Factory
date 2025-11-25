# config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

class Settings(BaseSettings):
    rabbitmq_url: str
    rabbitmq_queue_name: str

    class Config:
        # .env 파일에서 변수들을 로드합니다.
        env_file = '../../.env'

settings = Settings()
