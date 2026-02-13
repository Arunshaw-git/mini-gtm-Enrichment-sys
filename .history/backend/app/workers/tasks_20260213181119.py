from .celery_app import celery
import time

@celery.task(bind=True, max_retries=3)
def test_task(self, domain: str):
    try:
        print(f"Processing {domain}")
        time.sleep(5)
        print(f"Finished {domain}")
    except Exception as e:
        raise self.retry(exc=e, countdown=5)