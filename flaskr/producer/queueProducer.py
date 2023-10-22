from config import Config
from celery import Celery

config = Config()


celery_app = Celery('tasks', broker=f'{config.REDIS_BROKER_BASE_URL}/0')

TASK_POSTED, = config.TOPICS

@celery_app.task(name=TASK_POSTED)
def task_posted(task_json):
    print(TASK_POSTED)
    pass