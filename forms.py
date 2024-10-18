from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired

class RegisterJournalClubForm(FlaskForm):
    theme = StringField('Theme', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    submit = SubmitField('Register Journal Club')
