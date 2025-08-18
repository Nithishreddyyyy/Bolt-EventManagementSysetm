from flask import Blueprint, render_template
from routes.utils import login_required, roles_required, get_current_user

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
    return render_template("judge/dashboard.html", user_id=user_id, stats=stats)
