from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize DB
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.events import events_bp
    from routes.teams import teams_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(events_bp, url_prefix="/events")
    app.register_blueprint(teams_bp, url_prefix="/teams")

    @app.route("/")
    def home():
        return "🚀 Hackathon Platform Backend is running!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0',debug=True,port=8000)
