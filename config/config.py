import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


class Config:
    ENVIRONMENT = os.getenv('FLASK_ENV')
    REDIS_BROKER_BASE_URL=os.getenv('REDIS_BROKER_BASE_URL')
    SECRET_KEY=os.getenv('SECRET_KEY')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    APP_NAME=os.getenv('APP_NAME')