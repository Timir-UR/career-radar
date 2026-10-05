from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "career_radar",
    broker=settings.RABBITMQ_URL,
    include=["app.tasks.collect"],
)

celery_app.conf.beat_schedule = {
    "collect-remotive": {
        "task": "app.tasks.collect.collect_remotive",
        "schedule": 43200.0,
    },
    "collect-superjob": {
        "task": "app.tasks.collect.collect_superjob",
        "schedule": 3600.0,
    },
}

celery_app.conf.timezone = "UTC"
