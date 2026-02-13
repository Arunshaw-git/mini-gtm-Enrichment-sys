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

celery.autodiscover_tasks(["app.workers"])
    "app.workers.tasks.*": {"queue": "enrichment_queue"}
}