from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, JournalClub, DoctoralStudent, Attendance
from forms import RegisterJournalClubForm
from config import Config
from datetime import datetime, timedelta
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Set the SECRET_KEY for CSRF protection
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'b_5#y2L"F4Q8z\n\xec]/')

# Use the DATABASE_URL environment variable for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://kids_journalclub_x7v0_user:Mxj1Jl1YECnjyIltWQpLvIIfdt59o0VC@dpg-csb3ms2j1k6c73d0tvu0-a.frankfurt-postgres.render.com/kids_journalclub_x7v0')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    # Get the current date and calculate the date 7 days ago
    today = datetime.today().date()
    seven_days_ago = today - timedelta(days=7)

    # Query for journal clubs within the last 7 days and in the future
    journal_clubs = JournalClub.query.filter(JournalClub.date >= seven_days_ago).order_by(JournalClub.date.asc()).all()

    # Render the template and pass the filtered journal clubs
    return render_template('home.html', journal_clubs=journal_clubs)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        journal_club_id = request.form.get('journal_club_id')
        student_ids = request.form.getlist('student_ids')  # List of selected students

        # Debugging: Print the data received from the form
        print(f"Journal Club ID: {journal_club_id}")
        print(f"Selected Students: {student_ids}")

        # Register attendance for each selected student
        for student_id in student_ids:
            attendance = Attendance(student_id=student_id, journal_club_id=journal_club_id)
            db.session.add(attendance)

        db.session.commit()
        flash('Närvaro har registrerats.', 'success')
        return redirect(url_for('attendance'))

    # Fetch all journal clubs and students
    journal_clubs = JournalClub.query.all()
    students = DoctoralStudent.query.all()

    return render_template('attendance.html', journal_clubs=journal_clubs, students=students)


@app.route('/view_all_emails')
def view_all_emails():
    # Fetch all students' emails from the database
    students = DoctoralStudent.query.all()
    emails = "; ".join([student.ki_email for student in students])
    
    # Render the template and pass the emails
    return render_template('view_all_emails.html', emails=emails)

@app.route('/register_club', methods=['GET', 'POST'])
def register_club():
    form = RegisterJournalClubForm()
    if form.validate_on_submit():
        new_club = JournalClub(
            description=form.description.data,
            DOI=form.DOI.data,
            date=form.date.data,
            time=form.time.data,
            place=form.place.data
        )
        db.session.add(new_club)
        db.session.commit()
        flash('Journal Club registered successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('register_club.html', form=form)

@app.route('/view_students')
def view_students():
    students = DoctoralStudent.query.order_by(DoctoralStudent.end_date.asc()).all()
    return render_template('view_students.html', students=students)

@app.route('/register', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        unit = request.form['unit']
        ki_email = request.form['ki_email']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Check if the student already exists
        existing_student = DoctoralStudent.query.filter_by(first_name=first_name, last_name=last_name).first()
        if existing_student:
            flash('Denna student finns redan i databas', 'error')
            return redirect(url_for('register_student'))

        # Convert date strings to date objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None

        new_student = DoctoralStudent(
            first_name=first_name,
            last_name=last_name,
            unit=unit,
            ki_email=ki_email,
            start_date=start_date,
            end_date=end_date
        )

        db.session.add(new_student)
        db.session.commit()
        flash('Doktorand registrerad!', 'success')
        return redirect(url_for('view_students'))

    return render_template('register_student.html')

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = DoctoralStudent.query.get_or_404(student_id)
    allowed_units = [
        'Anestesi och Intensivvård', 'Hjärtmedicin', 'Infektionssjukdomar',
        'Kirurgi och urologi', 'Medicin', 'Medicinsk pedagogik', 'Neurologi',
        'Njurmedicin', 'Obstetrik och gynekologi', 'Ortopedi', 'Rehabiliteringsmedicin'
    ]
    if request.method == 'POST':
        student.unit = request.form['unit']
        db.session.commit()
        flash('Studenten har uppdaterats.', 'success')
        return redirect(url_for('view_students'))
    return render_template('edit_student.html', student=student, allowed_units=allowed_units)
    
@app.route('/register_attendance', methods=['GET', 'POST'])
def register_attendance():
    if request.method == 'POST':
        journal_club_id = request.form.get('journal_club_id')
        student_ids = request.form.getlist('student_ids')  # List of selected students

        for student_id in student_ids:
            # Check if this student is already registered for this journal club
            existing_attendance = Attendance.query.filter_by(student_id=student_id, journal_club_id=journal_club_id).first()
            
            if not existing_attendance:
                # Only add attendance if it's not a duplicate
                attendance = Attendance(student_id=student_id, journal_club_id=journal_club_id)
                db.session.add(attendance)

        # Commit after processing all students
        db.session.commit()
        flash('Närvaro har registrerats.', 'success')
        return redirect(url_for('attendance'))

    # Fetch all journal clubs and students for the form
    journal_clubs = JournalClub.query.all()
    students = DoctoralStudent.query.all()  # Ensure students are queried correctly
    
    return render_template('register_attendance.html', journal_clubs=journal_clubs, students=students)

@app.route('/edit_attendance/<int:attendance_id>', methods=['GET', 'POST'])
def edit_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    journal_clubs = JournalClub.query.all()
    students = DoctoralStudent.query.all()

    if request.method == 'POST':
        student_id = request.form['student_id']
        journal_club_id = request.form['journal_club_id']

        # Check for duplicates before saving
        existing_attendance = Attendance.query.filter_by(student_id=student_id, journal_club_id=journal_club_id).first()
        if existing_attendance and existing_attendance.id != attendance_id:
            flash('Studenten är redan registrerad för denna Journal Club.', 'error')
        else:
            attendance.journal_club_id = journal_club_id
            attendance.student_id = student_id
            db.session.commit()
            flash('Närvaro har uppdaterats.', 'success')
            return redirect(url_for('view_attendance'))

    return render_template('edit_attendance.html', attendance=attendance, journal_clubs=journal_clubs, students=students)

@app.route('/student_attendance/<int:student_id>')
def student_attendance(student_id):
    student = DoctoralStudent.query.get_or_404(student_id)
    attendances = Attendance.query.filter_by(student_id=student_id).all()
    
    return render_template('student_attendance.html', student=student, attendances=attendances)

@app.route('/journal_club_attendance/<int:journal_club_id>')
def journal_club_attendance(journal_club_id):
    journal_club = JournalClub.query.get_or_404(journal_club_id)
    attendances = Attendance.query.filter_by(journal_club_id=journal_club_id).all()

    return render_template('journal_club_attendance.html', journal_club=journal_club, attendances=attendances)

@app.route('/view_journal_clubs')
def view_journal_clubs():
    journal_clubs = JournalClub.query.all()
    return render_template('view_journal_clubs.html', journal_clubs=journal_clubs)

from datetime import datetime, time

@app.route('/edit_journal_club/<int:journal_club_id>', methods=['GET', 'POST'])
def edit_journal_club(journal_club_id):
    journal_club = JournalClub.query.get_or_404(journal_club_id)
    if request.method == 'POST':
        # Update all fields from the form
        journal_club.description = request.form['description']
        journal_club.place = request.form['place']
        journal_club.DOI = request.form['DOI']

        # Convert the date from string to a datetime.date object
        date_string = request.form['date']
        journal_club.date = datetime.strptime(date_string, '%Y-%m-%d').date()

        # Convert the time from string to a datetime.time object
        time_string = request.form['time']
        journal_club.time = datetime.strptime(time_string, '%H:%M').time()

        # Commit the changes
        db.session.commit()
        flash('Journal Club har uppdaterats.', 'success')
        return redirect(url_for('view_journal_clubs'))
    
    return render_template('edit_journal_club.html', journal_club=journal_club)

@app.route('/delete_journal_club/<int:journal_club_id>', methods=['POST'])
def delete_journal_club(journal_club_id):
    journal_club = JournalClub.query.get_or_404(journal_club_id)

    try:
        # Deleting attendance records before deleting the journal club
        attendances = Attendance.query.filter_by(journal_club_id=journal_club_id).all()
        for attendance in attendances:
            db.session.delete(attendance)

        # Now delete the journal club
        db.session.delete(journal_club)
        db.session.commit()
        flash('Journal Club har tagits bort.', 'success')
        return '', 200  # Return success
    except Exception as e:
        db.session.rollback()
        flash('Det gick inte att ta bort Journal Club.', 'error')
        return str(e), 400  # Return error if deletion fails

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = DoctoralStudent.query.get_or_404(student_id)
    
    try:
        # Deleting attendance records before deleting the student
        attendances = Attendance.query.filter_by(student_id=student_id).all()
        for attendance in attendances:
            db.session.delete(attendance)

        # Now delete the student
        db.session.delete(student)
        db.session.commit()
        flash('Studenten har tagits bort.', 'success')
        return '', 200  # Return success
    except Exception as e:
        db.session.rollback()
        flash('Det gick inte att ta bort studenten.', 'error')
        return str(e), 400  # Return error if deletion fails

@app.route('/delete_attendance/<int:attendance_id>', methods=['POST'])
def delete_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    try:
        db.session.delete(attendance)
        db.session.commit()
        return '', 200  # Return success
    except Exception as e:
        db.session.rollback()
        return str(e), 400  # Return error if deletion fails

if __name__ == '__main__':
    app.run(debug=True)