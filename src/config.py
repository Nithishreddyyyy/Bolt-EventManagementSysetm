import os

class Config:
    # Secret key for sessions
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")

    # Database URI (MySQL from Render/PlanetScale)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        "mysql+pymysql://root:test1234@localhost/hackdb"  # fallback for local dev
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT secret key
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "supersecretjwtkey")
