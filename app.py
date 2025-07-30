from flask import Flask, request, redirect, make_response, Response
from db_manager import (
    create_tables, add_student, add_grade, connect_db,
    subject_wise_topper, subject_average
)
import csv

app = Flask(__name__)
create_tables()

# 🔄 Prevent caching
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/')
def home():
    return (
        "<h1>🎓 Student Performance Tracker</h1>"
        "<p><a href='/add-student'>Add Student</a></p>"
        "<p><a href='/add-grade'>Add Grade</a></p>"
        "<p><a href='/students'>View All Students</a></p>"
        "<p><a href='/view-student'>View Student Details</a></p>"
        "<p><a href='/subject-topper'>Subject-wise Topper 🏆</a></p>"
        "<p><a href='/subject-average'>Subject-wise Class Average 📊</a></p>"
        "<p><a href='/export-grades'>Export Grades to CSV 📤</a></p>"
    )

@app.route('/add-student', methods=['GET', 'POST'])
def add_student_form():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        add_student(name, roll)
        return redirect('/')
    return '''
        <h2>Add Student</h2>
        <form method="post">
            Name: <input type="text" name="name"><br>
            Roll No: <input type="text" name="roll"><br>
            <button type="submit">Add Student</button>
        </form>
        <p><a href="/">Back</a></p>
    '''

@app.route('/add-grade', methods=['GET', 'POST'])
def add_grade_form():
    if request.method == 'POST':
        roll = request.form['roll']
        subject = request.form['subject']
        marks = float(request.form['marks'])
        add_grade(roll, subject, marks)
        return redirect('/')
    return '''
        <h2>Add Grade</h2>
        <form method="post">
            Roll No: <input type="text" name="roll"><br>
            Subject: <input type="text" name="subject"><br>
            Marks: <input type="number" step="any" name="marks"><br>
            <button type="submit">Submit Grade</button>
        </form>
        <p><a href="/">Back</a></p>
    '''

@app.route('/students')
def list_students():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT roll_number, name FROM students")
    rows = cur.fetchall()
    conn.close()

    html = "<h2>👥 All Students</h2><ul>"
    for roll, name in rows:
        html += f"<li>{roll} - {name}</li>"
    html += "</ul><p><a href='/'>Back to Home</a></p>"
    return html

@app.route('/view-student', methods=['GET', 'POST'])
def view_student():
    if request.method == 'POST':
        roll = request.form['roll']
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT name FROM students WHERE roll_number = ?", (roll,))
        student = cur.fetchone()

        if not student:
            return "<h2>❌ Student not found</h2><p><a href='/view-student'>Try again</a></p>"

        name = student[0]
        cur.execute("SELECT subject, grade FROM grades WHERE roll_number = ?", (roll,))
        grades = cur.fetchall()
        conn.close()

        html = f"<h2>📄 Report for {name} (Roll {roll})</h2><ul>"
        for subject, grade in grades:
            html += f"<li>{subject}: {grade}</li>"
        html += "</ul><p><a href='/'>Back</a></p>"

        return html

    return '''
        <h2>View Student Details</h2>
        <form method="post">
            Roll No: <input type="text" name="roll"><br>
            <button type="submit">Search</button>
        </form>
        <p><a href="/">Back</a></p>
    '''

@app.route('/subject-topper', methods=['GET', 'POST'])
def subject_topper():
    if request.method == 'POST':
        subject = request.form['subject']
        name, grade = subject_wise_topper(subject)
        if name:
            return f"<h2>🏆 Topper in {subject}: {name} ({grade} marks)</h2><p><a href='/'>Back</a></p>"
        else:
            return f"<h2>❌ No grades found for subject '{subject}'</h2><p><a href='/'>Back</a></p>"

    return '''
        <h2>Subject-wise Topper</h2>
        <form method="post">
            Subject: <input type="text" name="subject"><br>
            <button type="submit">Find Topper</button>
        </form>
        <p><a href="/">Back</a></p>
    '''

@app.route('/subject-average', methods=['GET', 'POST'])
def subject_avg():
    if request.method == 'POST':
        subject = request.form['subject']
        avg = subject_average(subject)
        if avg is not None:
            return f"<h2>📊 Class Average in {subject}: {avg:.2f}</h2><p><a href='/'>Back</a></p>"
        else:
            return f"<h2>❌ No grades found for subject '{subject}'</h2><p><a href='/'>Back</a></p>"

    return '''
        <h2>Subject-wise Class Average</h2>
        <form method="post">
            Subject: <input type="text" name="subject"><br>
            <button type="submit">Calculate</button>
        </form>
        <p><a href="/">Back</a></p>
    '''

@app.route('/export-grades')
def export_grades():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT students.roll_number, students.name, grades.subject, grades.grade
        FROM grades
        JOIN students ON students.roll_number = grades.roll_number
    """)
    data = cur.fetchall()
    conn.close()

    def generate():
        yield 'Roll Number,Name,Subject,Grade\n'
        for row in data:
            yield ','.join(map(str, row)) + '\n'

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=student_grades.csv"})

if __name__ == '__main__':
    app.run(debug=True, port=5500)