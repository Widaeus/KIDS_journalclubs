from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email

units = [
    ('Anestesi och Intensivvård', 'Anestesi och Intensivvård'),
    ('Hjärtmedicin', 'Hjärtmedicin'),
    ('Infektionssjukdomar', 'Infektionssjukdomar'),
    ('Kirurgi och urologi', 'Kirurgi och urologi'),
    ('Medicin', 'Medicin'),
    ('Medicinsk pedagogik', 'Medicinsk pedagogik'),
    ('Neurologi', 'Neurologi'),
    ('Njurmedicin', 'Njurmedicin'),
    ('Obstetrik och gynekologi', 'Obstetrik och gynekologi'),
    ('Ortopedi', 'Ortopedi'),
    ('Rehabiliteringsmedicin', 'Rehabiliteringsmedicin')
]

class RegisterJournalClubForm(FlaskForm):
    theme = StringField('Tema', validators=[DataRequired()])
    date = DateField('Datum', validators=[DataRequired()])
    time = TimeField('Tid', validators=[DataRequired()])
    place = StringField('Plats', validators=[DataRequired()])
    submit = SubmitField('Registrera')

class RegisterStudentForm(FlaskForm):
    first_name = StringField('Förnamn', validators=[DataRequired()])
    last_name = StringField('Efternamn', validators=[DataRequired()])
    unit = SelectField('Enhet', choices=units, validators=[DataRequired()])
    ki_email = StringField('KI E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Register Student')