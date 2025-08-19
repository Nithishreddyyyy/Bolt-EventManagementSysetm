from flask import Blueprint, render_template
from routes.utils import login_required, roles_required, get_current_user
from models import db
from models.event import Event
from sqlalchemy import text
from datetime import datetime

organizer_bp = Blueprint("organizer", __name__, url_prefix="/organizer")

@organizer_bp.route("/dashboard")
@login_required
@roles_required("organizer")
def dashboard():
    user_id, _ = get_current_user()
    # Events created by this organizer
    events_q = Event.query.filter_by(created_by=user_id)
    events_created = events_q.count()
    now = datetime.utcnow()
    active_events = events_q.filter(Event.start_date <= now, Event.end_date >= now).count()

    # Participants across organizer's events (distinct users in teams for those events)
    participants_total = 0
    try:
        sql = text(
            """
            SELECT COUNT(DISTINCT tm.user_id) AS cnt
            FROM Teams t
            JOIN TeamMembers tm ON tm.team_id = t.team_id
            JOIN Events e ON e.event_id = t.event_id
            WHERE e.created_by = :org_id
            """
        )
        res = db.session.execute(sql, {"org_id": user_id}).first()
        participants_total = int(res.cnt) if res and res.cnt is not None else 0
    except Exception:
        # Fallback if tables don't exist yet
        participants_total = 0

    # Registered teams across organizer's events
    teams_count = 0
    try:
        teams_sql = text(
            """
            SELECT COUNT(*) AS cnt
            FROM Teams t
            JOIN Events e ON e.event_id = t.event_id
            WHERE e.created_by = :org_id
            """
        )
        tr = db.session.execute(teams_sql, {"org_id": user_id}).first()
        teams_count = int(tr.cnt) if tr and tr.cnt is not None else 0
    except Exception:
        teams_count = 0

    # Submissions count from JudgingScores (distinct submission_id)
    submissions_count = 0
    try:
        subs_sql = text(
            """
            SELECT COUNT(DISTINCT submission_id) AS cnt
            FROM JudgingScores
            """
        )
        sr = db.session.execute(subs_sql).first()
        submissions_count = int(sr.cnt) if sr and sr.cnt is not None else 0
    except Exception:
        submissions_count = 0

    # Revenue from sponsors linked to organizer's events
    revenue_total = 0
    try:
        revenue_sql = text(
            """
            SELECT COALESCE(SUM(es.amount), 0) AS total
            FROM EventSponsors es
            JOIN Events e ON e.event_id = es.event_id
            WHERE e.created_by = :org_id
            """
        )
        rr = db.session.execute(revenue_sql, {"org_id": user_id}).first()
        revenue_total = float(rr.total) if rr and rr.total is not None else 0.0
    except Exception:
        revenue_total = 0.0

    stats = {
        "events_created": events_created,
        "active_events": active_events,
        "participants_total": participants_total,
        # Additional metrics used by organizer UI
        "total_hackathons": events_created,
        "teams": teams_count,
        "submissions": submissions_count,
        "revenue": revenue_total,
    }
    events = events_q.order_by(Event.start_date.desc()).limit(10).all()
    # Render the provided organizer dashboard template
    return render_template("organizer/o-index.html", user_id=user_id, stats=stats, events=events)
