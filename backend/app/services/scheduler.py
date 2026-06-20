from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from app.services.news_ingestion import run_ingestion


def scheduled_ingestion():
    print(f"Scheduled ingestion started at {datetime.now()}...")
    try:
        run_ingestion()
    except Exception as e:
        print(f"Scheduler error: {e}")


scheduler = BlockingScheduler()

scheduler.add_job(
    scheduled_ingestion,
    trigger="interval",
    minutes=1,
)


if __name__ == "__main__":
    print("Scheduler started...")
    scheduler.start()