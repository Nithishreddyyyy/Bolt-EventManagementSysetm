from app import create_app, db
from sqlalchemy import text   # <-- import text

app = create_app()

with app.app_context():
    try:
        result = db.session.execute(text("SELECT 1")).scalar()
        print("✅ Database connection working, result =", result)
    except Exception as e:
        print("❌ Database connection failed:", str(e))
