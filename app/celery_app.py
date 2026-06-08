from celery import Celery
from app.core.config import settings
from celery.schedules import crontab

celery_app = Celery("app", broker=settings.redis.url, backend=settings.redis.url)
celery_app.autodiscover_tasks(["app"])

celery_app.conf.beat_schedule = {
    "cleanup-revoked-tokens": {
        "task": "app.tasks.cleanup_revoked_tokens",
        "schedule": crontab(hour=0, minute=0),
    },
    "check-deadline-tasks": {
        "task": "app.tasks.check_deadline_tasks",
        "schedule": crontab(minute=0),
    },
}

celery_app.conf.update(task_serializer="json", result_serializer="json")
