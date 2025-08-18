from models import db

class Event(db.Model):
    __tablename__ = "Events"

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    theme = db.Column(db.String(100))
    rules = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    prizes = db.Column(db.JSON)
    created_by = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
