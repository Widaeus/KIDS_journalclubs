from app import db, app, DoctoralStudent

# Create an application context
with app.app_context():
    # Now you can run database queries
    students = DoctoralStudent.query.all()
    for student in students:
        print(student.first_name, student.last_name, student.ki_email, student.unit, student.start_date, student.end_date)
