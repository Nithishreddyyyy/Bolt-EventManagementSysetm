from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db   # ✅ import db here

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    # Secret key for flash messages
    app.secret_key = "supersecret"

    # Initialize extensions
    db.init_app(app)       # ✅ attaches db to app
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.participant import participant_bp
    from routes.events import events_bp
    from routes.judge import judge_bp
    from routes.organizer import organizer_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(participant_bp)
    app.register_blueprint(events_bp, url_prefix="/api/events")
    app.register_blueprint(judge_bp)
    app.register_blueprint(organizer_bp)

    @app.route("/")
    def home():
        return render_template("login.html")

    @app.route("/register")
    def register():
        return render_template("create_account.html")

    # Health / readiness endpoint
    @app.route("/health")
    def health():
        return jsonify(status="ok"), 200

    # Example error handlers
    @app.errorhandler(404)
    def not_found(err):  # pragma: no cover simple handler
        return render_template("login.html"), 404

    @app.errorhandler(500)
    def server_error(err):  # pragma: no cover simple handler
        return jsonify(error="server_error"), 500

    # Provide shell context for flask shell
    @app.shell_context_processor
    def shell_ctx():
        return {"db": db}

    @app.cli.command("seed-events")
    def seed_events():  # pragma: no cover utility
        """Seed some sample events for quick local testing (idempotent)."""
        from models.event import Event
        from models.user import User
        with app.app_context():
            # Ensure at least one organizer user exists
            organizer = User.query.filter_by(role="organizer").first()
            if not organizer:
                organizer = User(name="Demo Organizer", email="org@example.com", password="pass", role="organizer")
                db.session.add(organizer)
                db.session.commit()
            existing = Event.query.filter_by(created_by=organizer.user_id).count()
            if existing >= 3:
                print("Seed events already present; skipping.")
                return
            base = datetime.utcnow()
            samples = [
                ("AI Innovation Challenge", base - timedelta(days=2), base + timedelta(days=3)),
                ("FinTech Sprint", base + timedelta(days=5), base + timedelta(days=8)),
                ("Open Source Marathon", base - timedelta(days=10), base - timedelta(days=5)),
            ]
            for name, start, end in samples:
                e = Event(name=name, theme="General", rules="online allowed", start_date=start, end_date=end, prizes=None, created_by=organizer.user_id)
                db.session.add(e)
            db.session.commit()
            print("Seeded sample events.")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0',debug=True,port=5001)
