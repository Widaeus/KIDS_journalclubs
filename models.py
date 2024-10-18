from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class JournalClub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    place = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<JournalClub {self.theme}>'

class DoctoralStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<DoctoralStudent {self.name}>'
