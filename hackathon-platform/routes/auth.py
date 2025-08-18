from flask import Blueprint, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "Login endpoint (to be implemented)"})

@auth_bp.route("/signup", methods=["POST"])
def signup():
    return jsonify({"message": "Signup endpoint (to be implemented)"})
