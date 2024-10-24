from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    reminder = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Event {self.title}>'
