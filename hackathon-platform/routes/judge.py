from flask import Blueprint, render_template
from routes.utils import login_required, roles_required, get_current_user
from models.event import Event

judge_bp = Blueprint("judge", __name__, url_prefix="/judge")

@judge_bp.route("/dashboard")
@login_required
@roles_required("judge")
def dashboard():
    user_id, _ = get_current_user()
    # TODO: Load assigned events/submissions for this judge
    stats = {
        "assigned_events": 0,
        "pending_reviews": 0,
        "completed_reviews": 0,
    }
    return render_template("judge/j-dashboard.html", user_id=user_id, stats=stats)

@judge_bp.route("/events")
@login_required
@roles_required("judge")
def events():
    events = Event.query.order_by(Event.start_date.asc()).all()
    return render_template("judge/j-events.html", events=events)

@judge_bp.route("/projects")
@login_required
@roles_required("judge")
def projects():
    return render_template("judge/j-projects.html")

@judge_bp.route("/leaderboard")
@login_required
@roles_required("judge")
def leaderboard():
    return render_template("judge/j-leaderboard.html")

@judge_bp.route("/announcements")
@login_required
@roles_required("judge")
def announcements():
    return render_template("judge/j-announcement.html")
