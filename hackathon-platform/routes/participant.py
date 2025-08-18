from flask import Blueprint, render_template
from types import SimpleNamespace
from routes.utils import login_required, roles_required, get_current_user
from models import db
from sqlalchemy import text

try:
    from models.event import Event
except Exception:
    Event = None  # fallback if model not available

participant_bp = Blueprint("participant", __name__, url_prefix="/participant")

@participant_bp.route("/dashboard")
@login_required
@roles_required("participant")
def dashboard():
    events_count = 0
    teams_count = 0
    submissions_count = 0
    announcements_count = 0
    recent_events = []
    user_id, role = get_current_user()

    if Event is not None:
        recent_events = Event.query.order_by(Event.event_id.desc()).limit(5).all()
        events_count = Event.query.count()

    event_progress = {"progress_percentage": 0}

    return render_template(
        "participants/P-Dashboard.html",
        events_count=events_count,
        teams_count=teams_count,
        submissions_count=submissions_count,
        announcements_count=announcements_count,
        recent_events=recent_events,
        event=event_progress,
        user_id=user_id,
    )

@participant_bp.route("/events")
@login_required
@roles_required("participant")
def events():
    events = []
    if Event is not None:
        events = Event.query.order_by(Event.start_date.asc()).all()
    return render_template("participants/P-Events.html", events=events)

@participant_bp.route("/teams")
@login_required
@roles_required("participant")
def teams():
    teams = []
    user_id, _ = get_current_user()
    # Fetch teams for the logged-in participant without ORM models
    try:
        sql = text(
            """
            SELECT t.team_id, t.team_name, t.event_id, t.leader_id
            FROM TeamMembers tm
            JOIN Teams t ON t.team_id = tm.team_id
            WHERE tm.user_id = :uid
            ORDER BY t.team_id ASC
            """
        )
        rows = db.session.execute(sql, {"uid": user_id}).mappings().all()
        teams = [dict(row) for row in rows]
    except Exception:
        teams = []
    return render_template("participants/P-team.html", teams=teams, user_id=user_id)

@participant_bp.route("/submissions")
@login_required
@roles_required("participant")
def submissions():
    submissions = []
    return render_template("participants/P-Submissions.html", submissions=submissions)

@participant_bp.route("/announcements")
@login_required
@roles_required("participant")
def announcements():
    announcements = []
    return render_template("participants/P-announcement.html", announcements=announcements)
