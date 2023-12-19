from celery import Celery

from apps.api.crawler.youtube_crawler.youtube_crawler import YoutubeCrawlerJob
from core.settings import settings

celery = Celery(
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL
)
celery.autodiscover_tasks([
    'celery.tasks'
])


@celery.task
def add(first, second):
    print("Task executed!", first+second)

@celery.task
def run_script2(keywords):
    return YoutubeCrawlerJob.run_script2(keywords=keywords)
