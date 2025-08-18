from flask import Blueprint, jsonify

teams_bp = Blueprint("teams", __name__)

@teams_bp.route("/register", methods=["POST"])
def register_team():
    return jsonify({"message": "Team registration endpoint (to be implemented)"})
