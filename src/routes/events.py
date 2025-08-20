from flask import Blueprint, request, jsonify
from models import db
from models.event import Event
from datetime import datetime
import json

events_bp = Blueprint("events", __name__)

@events_bp.route("/create", methods=["POST"]) 
def create_event():
    data = request.get_json(force=True)

    # Parse prizes which may come as list or JSON string
    prizes = data.get("prizes")
    if isinstance(prizes, str):
        try:
            prizes = json.loads(prizes)
        except json.JSONDecodeError:
            prizes = None

    new_event = Event(
        name=data["name"],
        theme=data.get("theme", ""),
        rules=data.get("rules", ""),
        start_date=datetime.fromisoformat(data["start_date"].replace(" ", "T")),
        end_date=datetime.fromisoformat(data["end_date"].replace(" ", "T")),
        prizes=prizes,
        created_by=int(data["created_by"]),
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Event created successfully!", "event_id": new_event.event_id})

@events_bp.route("/all", methods=["GET"]) 
def get_events():
    events = Event.query.order_by(Event.start_date.asc()).all()
    return jsonify([
        {
            "event_id": e.event_id,
            "name": e.name,
            "theme": e.theme,
            "rules": e.rules,
            "start_date": e.start_date.isoformat() if e.start_date else None,
            "end_date": e.end_date.isoformat() if e.end_date else None,
            "prizes": e.prizes,
            "created_by": e.created_by,
        }
        for e in events
    ])
