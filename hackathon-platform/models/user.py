import uuid
from datetime import datetime
from models import db   # import db from models, do NOT create new one

class User(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)   # plain text password
    role = db.Column(db.Enum("participant", "judge", "organizer"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
