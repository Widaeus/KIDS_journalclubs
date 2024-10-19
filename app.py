from flask import Flask, render_template, redirect, url_for, flash
from models import db, JournalClub, DoctoralStudent
from forms import RegisterJournalClubForm, RegisterStudentForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_club():
    form = RegisterJournalClubForm()
    if form.validate_on_submit():
        new_club = JournalClub(
            theme=form.theme.data,
            date=form.date.data,
            time=form.time.data,
            place=form.place.data
        )
        db.session.add(new_club)
        db.session.commit()
        flash('Journal Club Registered!', 'success')
        return redirect(url_for('view_emails'))
    return render_template('register_club.html', form=form)

@app.route('/view_emails')
def view_emails():
    students = DoctoralStudent.query.all()
    return render_template('view_emails.html', students=students)

@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    form = RegisterStudentForm()
    if form.validate_on_submit():
        new_student = DoctoralStudent(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            institution=form.institution.data,
            ki_email=form.ki_email.data
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student Registered!', 'success')
        return redirect(url_for('view_emails'))
    return render_template('register_student.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
