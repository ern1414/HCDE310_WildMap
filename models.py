# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

db = SQLAlchemy()
pst_tz = ZoneInfo('America/Los_Angeles')  # pst timezone

# model for storing animal sightings
class Sighting(db.Model):
    __tablename__ = 'sightings'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    species     = db.Column(db.String(80), nullable=False)
    # timezone-aware timestamp default to now in pst
    time_spotted = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(tz=pst_tz)
    )
    latitude  = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    location  = db.Column(db.String(120), nullable=False)

    # readable repr for debugging
    def __repr__(self):
        return f'<Sighting {self.species} @ {self.location}>'
