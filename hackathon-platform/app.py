from flask import Flask, render_template
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
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def home():
        return render_template("login.html")

    @app.route("/register")
    def register():
        return render_template("create_account.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
