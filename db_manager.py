import sqlite3

def connect_db():
    return sqlite3.connect("students.db")

def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_number TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            roll_number TEXT,
            subject TEXT,
            grade REAL,
            FOREIGN KEY (roll_number) REFERENCES students (roll_number)
        )
    """)
    conn.commit()
    conn.close()

def add_student(name, roll):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO students (roll_number, name) VALUES (?, ?)", (roll, name))
    conn.commit()
    conn.close()

def add_grade(roll, subject, marks):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO grades (roll_number, subject, grade) VALUES (?, ?, ?)", (roll, subject, marks))
    conn.commit()
    conn.close()

def subject_wise_topper(subject):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT students.name, grades.grade
        FROM grades
        JOIN students ON grades.roll_number = students.roll_number
        WHERE subject = ?
        ORDER BY grade DESC
        LIMIT 1
    """, (subject,))
    result = cur.fetchone()
    conn.close()
    return result if result else (None, None)

def subject_average(subject):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT AVG(grade) FROM grades WHERE subject = ?", (subject,))
    result = cur.fetchone()[0]
    conn.close()
    return result