from flask import Blueprint, request, jsonify
from models import db
from models.event import Event

events_bp = Blueprint("events", __name__)

@events_bp.route("/create", methods=["POST"])
def create_event():
    data = request.json
    new_event = Event(
        name=data["name"],
        theme=data.get("theme", ""),
        rules=data.get("rules", "")
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Event created successfully!"})

@events_bp.route("/all", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([{"id": e.id, "name": e.name, "theme": e.theme} for e in events])
