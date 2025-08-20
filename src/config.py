import os

class Config:
    # Secret key for sessions
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")

    # Database URI (SQLite for local/dev)
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'app.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT secret key
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "supersecretjwtkey")
