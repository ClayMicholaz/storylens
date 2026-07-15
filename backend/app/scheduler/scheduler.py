from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from app.ingestion.pipeline import run_ingestion


def scheduled_ingestion():
    print(f"Scheduled ingestion started at {datetime.now()}...")
    try:
        run_ingestion()
    except Exception as e:
        print(f"Scheduler error: {e}")


# Create scheduler but don't start it - will be started by FastAPI lifespan
scheduler = BackgroundScheduler()

# Add the job - scheduler will be started later
scheduler.add_job(
    scheduled_ingestion,
    trigger="interval",
    minutes=1,
    max_instances=1,
    coalesce=True,
    misfire_grace_time=30,
)


if __name__ == "__main__":
    print("Scheduler started...")
    scheduler.start()
