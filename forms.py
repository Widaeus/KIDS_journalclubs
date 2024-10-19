from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Email

class RegisterJournalClubForm(FlaskForm):
    theme = StringField('Tema', validators=[DataRequired()])
    date = DateField('Datum', validators=[DataRequired()])
    time = TimeField('Tid', validators=[DataRequired()])
    place = StringField('Plats', validators=[DataRequired()])
    submit = SubmitField('Registrera')

class RegisterStudentForm(FlaskForm):
    first_name = StringField('Förnamn', validators=[DataRequired()])
    last_name = StringField('Efternamn', validators=[DataRequired()])
    unit = StringField('Enhet', validators=[DataRequired()])
    ki_email = StringField('KI E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Register Student')