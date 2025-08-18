from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login_page"))
        return view_func(*args, **kwargs)
    return wrapper


def roles_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            role = session.get("role")
            if role not in roles:
                flash("You are not authorized to access this page.", "danger")
                return redirect(url_for("auth.login_page"))
            return view_func(*args, **kwargs)
        return wrapper
    return decorator


def get_current_user():
    """Return (user_id, role) tuple from the session, or (None, None)."""
    return session.get("user_id"), session.get("role")
