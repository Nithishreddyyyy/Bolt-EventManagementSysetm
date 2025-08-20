from flask import Blueprint, render_template
from routes.utils import login_required, roles_required, get_current_user
from models import db
from models.event import Event
from sqlalchemy import text
from datetime import datetime, timedelta

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


@organizer_bp.route("/events")
@login_required
@roles_required("organizer")
def events_page():
    """Render dynamic events list for the organizer passing raw Event models."""
    user_id, _ = get_current_user()
    events = Event.query.filter_by(created_by=user_id).order_by(Event.start_date.desc()).all()
    return render_template("organizer/o-events.html", events=events, now=datetime.utcnow(), timedelta=timedelta)


@organizer_bp.route("/participants")
@login_required
@roles_required("organizer")
def participants_page():
    """Render participants across the organizer's events."""
    user_id, _ = get_current_user()
    participants = []
    try:
        sql = text(
            """
            SELECT DISTINCT u.user_id, u.name AS user_name, u.email, 
                   t.team_id, t.team_name AS team_name,
                   e.event_id, e.name AS event_name, e.start_date, e.end_date
            FROM Teams t
            JOIN TeamMembers tm ON tm.team_id = t.team_id
            JOIN Users u ON u.user_id = tm.user_id
            JOIN Events e ON e.event_id = t.event_id
            WHERE e.created_by = :org_id
            ORDER BY e.start_date DESC
            """
        )
        rows = db.session.execute(sql, {"org_id": user_id}).mappings().all()
        now = datetime.utcnow()
        for r in rows:
            # Derive status from event timing
            start = r.get("start_date")
            end = r.get("end_date")
            if start and end:
                if start > now:
                    status = "Upcoming"; badge = "warning"
                elif end < now:
                    status = "Completed"; badge = "secondary"
                else:
                    status = "Active"; badge = "success"
            else:
                status = "Confirmed"; badge = "primary"
            participants.append({
                "user_name": r.get("user_name"),
                "email": r.get("email"),
                "team_name": r.get("team_name") or f"Team #{r.get('team_id')}",
                "event_name": r.get("event_name"),
                "status": status,
                "badge": badge,
            })
    except Exception:
        # If schema mismatch / tables absent, return empty list gracefully
        participants = []

    return render_template("organizer/o-participants.html", participants=participants)


@organizer_bp.route("/teams")
@login_required
@roles_required("organizer")
def teams_page():
    """Render teams with member counts for organizer's events."""
    user_id, _ = get_current_user()
    teams = []
    try:
        sql = text(
            """
            SELECT t.team_id, t.team_name AS team_name, e.name AS event_name,
                   e.start_date, e.end_date,
                   COUNT(tm.user_id) AS member_count
            FROM Teams t
            JOIN Events e ON e.event_id = t.event_id
            LEFT JOIN TeamMembers tm ON tm.team_id = t.team_id
            WHERE e.created_by = :org_id
            GROUP BY t.team_id, t.team_name, e.name, e.start_date, e.end_date
            ORDER BY e.start_date DESC
            """
        )
        rows = db.session.execute(sql, {"org_id": user_id}).mappings().all()
        now = datetime.utcnow()
        for r in rows:
            start = r.get("start_date"); end = r.get("end_date")
            if start and end:
                if start > now:
                    status = "Upcoming"; badge = "warning"
                elif end < now:
                    status = "Completed"; badge = "secondary"
                else:
                    status = "Active"; badge = "success"
            else:
                status = "Active"; badge = "primary"
            teams.append({
                "team_name": r.get("team_name") or f"Team #{r.get('team_id')}",
                "event_name": r.get("event_name"),
                "member_count": r.get("member_count", 0),
                "status": status,
                "badge": badge,
            })
    except Exception:
        teams = []

    return render_template("organizer/o-teams.html", teams=teams)


@organizer_bp.route("/revenue")
@login_required
@roles_required("organizer")
def revenue_page():
    """Revenue analytics sourced from EventSponsors."""
    user_id, _ = get_current_user()
    revenue_rows = []
    total_revenue = 0.0
    sponsor_total = 0.0
    try:
        sql = text(
            """
            SELECT e.event_id, e.name AS event_name,
                   COALESCE(SUM(es.amount),0) AS sponsor_amount
            FROM Events e
            LEFT JOIN EventSponsors es ON es.event_id = e.event_id
            WHERE e.created_by = :org_id
            GROUP BY e.event_id, e.name
            ORDER BY e.start_date DESC
            """
        )
        rows = db.session.execute(sql, {"org_id": user_id}).mappings().all()
        for r in rows:
            amt = float(r.get("sponsor_amount") or 0.0)
            sponsor_total += amt
            revenue_rows.append({
                "event_name": r.get("event_name"),
                "sponsor_amount": amt,
            })
        total_revenue = sponsor_total  # If later you add ticket sales, adjust here
    except Exception:
        revenue_rows = []
    events_count = len(revenue_rows) or 1
    avg_revenue = total_revenue / events_count
    # Simple chart datasets (line uses amounts order, pie sponsors vs remainder)
    chart_data = {
        "line": [row["sponsor_amount"] for row in revenue_rows][:10],
        "pie": [sponsor_total, max(total_revenue - sponsor_total, 0)],
    }
    stats = {
        "total_revenue": total_revenue,
        "avg_revenue": avg_revenue,
        "sponsor_total": sponsor_total,
    }
    return render_template("organizer/o-revenue.html", revenue_rows=revenue_rows, stats=stats, chart_data=chart_data)


@organizer_bp.route("/judging")
@login_required
@roles_required("organizer")
def judging_page():
    """Judging analytics from JudgingScores and judge users."""
    user_id, _ = get_current_user()
    total_judges = 0
    evaluations = 0
    pending = 0
    judge_rows = []
    try:
        # Count judges
        judges_sql = text("SELECT COUNT(*) AS cnt FROM Users WHERE role = 'judge'")
        jr = db.session.execute(judges_sql).first()
        total_judges = int(jr.cnt) if jr and jr.cnt is not None else 0
        # Evaluations aggregate
        eval_sql = text("SELECT COUNT(*) AS cnt FROM JudgingScores")
        er = db.session.execute(eval_sql).first()
        evaluations = int(er.cnt) if er and er.cnt is not None else 0
        # Teams under this organizer (potential workload proxy)
        team_sql = text(
            """
            SELECT COUNT(*) AS cnt
            FROM Teams t JOIN Events e ON e.event_id = t.event_id
            WHERE e.created_by = :org_id
            """
        )
        tr = db.session.execute(team_sql, {"org_id": user_id}).first()
        teams_count = int(tr.cnt) if tr and tr.cnt is not None else 0
        potential = total_judges * teams_count
        pending = max(potential - evaluations, 0)
        # Judge performance rows
        performance_sql = text(
            """
            SELECT u.user_id, u.name AS judge_name,
                   COUNT(js.score_id) AS evals,
                   COALESCE(ROUND(AVG(js.score),2),0) AS avg_score
            FROM Users u
            LEFT JOIN JudgingScores js ON js.judge_id = u.user_id
            WHERE u.role = 'judge'
            GROUP BY u.user_id, u.name
            ORDER BY evals DESC
            """
        )
        prow = db.session.execute(performance_sql).mappings().all()
        for r in prow:
            judge_rows.append({
                "judge_name": r.get("judge_name"),
                "evals": int(r.get("evals") or 0),
                "avg_score": r.get("avg_score") or 0,
            })
    except Exception:
        judge_rows = []
    stats = {
        "total_judges": total_judges,
        "evaluations": evaluations,
        "pending": pending,
    }
    line_vals = [r["evals"] for r in judge_rows][:10]
    pie_vals = [r["evals"] for r in judge_rows[:4]]
    chart_data = {"line": line_vals, "pie": pie_vals}
    return render_template("organizer/o-judging.html", stats=stats, judge_rows=judge_rows, chart_data=chart_data)


@organizer_bp.route("/settings")
@login_required
@roles_required("organizer")
def settings_page():
    return render_template("organizer/o-settings.html")
