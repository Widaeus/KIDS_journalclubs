from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class JournalClub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    DOI = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    place = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<JournalClub {self.theme}>'

class DoctoralStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(150), nullable=False)
    ki_email = db.Column(db.String(120), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<DoctoralStudent {self.first_name} {self.last_name}>'