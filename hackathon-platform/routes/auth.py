from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models import db   # ✅ import db from models, do NOT create new one

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

        # ⚠️ plain text check (only for testing)
        if user and user.password == password:   # <-- use your actual password column name here
            print(f"✅ Login successful for {user.email}")
            session["user_id"] = user.user_id   # store logged-in user
            flash("Login successful!", "success")
            #return redirect(url_for("auth.login_page"))
        else:
            print(f"❌ Failed login attempt for {username_or_email}")
            flash("Invalid username or password!", "danger")
            return redirect(url_for("auth.login_page"))

    return render_template("login.html")
