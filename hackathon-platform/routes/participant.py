from flask import Blueprint, render_template, session, flash, redirect, url_for, request
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
    current_user_name = None
    try:
        from models.user import User
        if user_id:
            user_obj = User.query.get(user_id)
            if user_obj:
                current_user_name = user_obj.name
    except Exception:
        pass

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
    current_user_name=current_user_name,
    )

@participant_bp.route("/events")
@login_required
@roles_required("participant")
def events():
    events = []
    if Event is not None:
        events = Event.query.order_by(Event.start_date.asc()).all()
    current_user_name = session.get('user_name')
    return render_template("participants/P-Events.html", events=events, current_user_name=current_user_name)

@participant_bp.route("/teams")
@login_required
@roles_required("participant")
def teams():
    teams = []
    user_id, _ = get_current_user()
    # 1. Get all teams the user is a part of
    user_teams = []
    try:
        user_teams_sql = text(
            """
            SELECT DISTINCT t.team_id, t.team_name, t.leader_id, e.name as event_name
            FROM TeamMembers tm
            JOIN Teams t ON tm.team_id = t.team_id
            JOIN Events e ON t.event_id = e.event_id
            WHERE tm.user_id = :uid
            ORDER BY t.team_id
            """
        )
        user_teams_rows = db.session.execute(user_teams_sql, {"uid": user_id}).mappings().all()
        user_teams = [dict(row) for row in user_teams_rows]

        # 2. For each team, get all its members
        team_ids = [team['team_id'] for team in user_teams]
        if team_ids:
            members_sql = text(
                """
                SELECT tm.team_id, u.name, tm.role
                FROM TeamMembers tm
                JOIN Users u ON tm.user_id = u.user_id
                WHERE tm.team_id IN :team_ids
                ORDER BY tm.team_id, u.name
                """
            )
            members_rows = db.session.execute(members_sql, {"team_ids": tuple(team_ids)}).mappings().all()
            
            # 3. Attach members to their respective teams
            for team in user_teams:
                team['members'] = [member for member in members_rows if member['team_id'] == team['team_id']]

    except Exception as e:
        print(f"Error fetching team details: {e}") # for debugging
        user_teams = []

    teams = user_teams # Use the new structure
    current_user_name = session.get('user_name')
    return render_template("participants/P-team.html", teams=teams, user_id=user_id, current_user_name=current_user_name)

@participant_bp.route("/submissions")
@login_required
@roles_required("participant")
def submissions():
    submissions = []
    current_user_name = session.get('user_name')
    return render_template("participants/P-Submissions.html", submissions=submissions, current_user_name=current_user_name)

@participant_bp.route("/announcements")
@login_required
@roles_required("participant")
def announcements():
    announcements = []
    current_user_name = session.get('user_name')
    return render_template("participants/P-announcement.html", announcements=announcements, current_user_name=current_user_name)


@participant_bp.route("/team/<int:team_id>")
@login_required
@roles_required("participant")
def team_details(team_id):
    user_id, _ = get_current_user()
    team_info = None

    try:
        # 1. Verify the current user is a member of this team
        membership_check_sql = text("""
            SELECT 1 FROM TeamMembers WHERE team_id = :team_id AND user_id = :user_id
        """)
        is_member = db.session.execute(membership_check_sql, {"team_id": team_id, "user_id": user_id}).scalar()

        if not is_member:
            flash("You are not authorized to view this team.", "danger")
            return redirect(url_for('participant.teams'))

        # 2. Get team details and members
        team_sql = text("""
            SELECT t.team_id, t.team_name, e.name as event_name, u_leader.name as leader_name
            FROM Teams t
            JOIN Events e ON t.event_id = e.event_id
            JOIN Users u_leader ON t.leader_id = u_leader.user_id
            WHERE t.team_id = :team_id
        """)
        team_info = db.session.execute(team_sql, {"team_id": team_id}).mappings().first()

        if team_info:
            members_sql = text("""
                SELECT u.name, tm.role
                FROM TeamMembers tm
                JOIN Users u ON tm.user_id = u.user_id
                WHERE tm.team_id = :team_id
                ORDER BY u.name
            """)
            members = db.session.execute(members_sql, {"team_id": team_id}).mappings().all()
            team_info = dict(team_info)
            team_info['members'] = members

    except Exception as e:
        print(f"Error fetching team details: {e}")
        team_info = None

    current_user_name = session.get('user_name')
    return render_template("participants/P-team-details.html", team=team_info, current_user_name=current_user_name)
