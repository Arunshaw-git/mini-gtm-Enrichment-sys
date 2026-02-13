from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery = Celery(
    "mini_gtm",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.task_routes = {
    "app.workers.tasks.*": {"queue": "enrichment_queue"}
}