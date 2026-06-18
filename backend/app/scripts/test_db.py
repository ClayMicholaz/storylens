from sqlalchemy import text
from app.database.session import SessionLocal

db = SessionLocal()

try:
    db.execute(text("SELECT 1"))
    print("Database connection successful.")
finally:
    db.close()