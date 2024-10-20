from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from models import db, JournalClub, DoctoralStudent
from forms import RegisterJournalClubForm, RegisterStudentForm
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

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
    if request.method == 'POST':
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.unit = request.form['unit']
        student.ki_email = request.form['ki_email']

        # Convert the start_date and end_date strings to date objects
        student.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        student.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date() if request.form['end_date'] else None

        db.session.commit()
        flash('Doktorandens information har uppdaterats.')
        return redirect(url_for('view_students'))
    
    return render_template('edit_student.html', student=student)


@app.route('/delete_student/<int:student_id>', methods=['POST', 'GET'])
def delete_student(student_id):
    student = DoctoralStudent.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Doktoranden har tagits bort.')
    return redirect(url_for('view_students'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/api/journal_clubs')
def get_journal_clubs():
    journal_clubs = JournalClub.query.all()  # Fetch all journal clubs from the database
    events = []
    for club in journal_clubs:
        events.append({
            'title': club.description,  # Assuming 'description' is the title
            'start': club.date.isoformat(),  # The 'date' field
            'time': club.time.strftime('%H:%M:%S'),  # The 'time' field
            'place': club.place,  # The 'place' field
            'DOI': club.DOI  # The 'DOI' field, if needed
        })
    return jsonify(events)
