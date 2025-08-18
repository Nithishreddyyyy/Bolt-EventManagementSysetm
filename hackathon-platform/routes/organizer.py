from flask import Blueprint, render_template
from routes.utils import login_required, roles_required, get_current_user

organizer_bp = Blueprint("organizer", __name__, url_prefix="/organizer")

@organizer_bp.route("/dashboard")
@login_required
@roles_required("organizer")
def dashboard():
    user_id, _ = get_current_user()
    # TODO: Load events created by this organizer and stats
    stats = {
        "events_created": 0,
        "active_events": 0,
        "participants_total": 0,
    }
    return render_template("organizer/dashboard.html", user_id=user_id, stats=stats)
