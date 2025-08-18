import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret_key"
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:test1234@localhost/hackathon_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
