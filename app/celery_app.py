from celery import Celery
from app.core.config import settings

celery_app = Celery("app", broker=settings.redis.url, backend=settings.redis.url)
celery_app.autodiscover_tasks(["app"])
celery_app.conf.update(task_serializer="json", result_serializer="json")
