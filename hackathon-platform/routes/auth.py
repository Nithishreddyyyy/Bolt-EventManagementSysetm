from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models import db   # import db from models, do NOT create new one

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username_or_email = request.form.get("username")
        password = request.form.get("password")

        # find user by email or name
        user = User.query.filter(
            (User.email == username_or_email) | (User.name == username_or_email)
        ).first()

        # plain text check (only for testing)
        if user and user.password == password:   # use your actual password column name here
            print(f" Login successful for {user.email}")
            session["user_id"] = user.user_id   # store logged-in user
            flash("Login successful!", "success")
            #return redirect(url_for("auth.login_page"))
        else:
            print(f" Failed login attempt for {username_or_email}")
            flash("Invalid username or password!", "danger")
            return redirect(url_for("auth.login_page"))

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        role = request.form.get("role", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # basic validations
        if not name or not email or not role or not password:
            flash("All fields are required.", "warning")
            return redirect(url_for("auth.register"))
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))
        if role not in ["participant", "judge", "organizer"]:
            flash("Invalid role selected.", "warning")
            return redirect(url_for("auth.register"))

        # check if user already exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered. Please login or use another email.", "warning")
            return redirect(url_for("auth.register"))

        # create user ( plain text password; replace with hashing in production)
        user = User(name=name, email=email, role=role, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("auth.login_page"))

    # GET -> show form
    return render_template("create_account.html")
