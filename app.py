# Minimal PostgreSQL CRUD app for `students` table.
# - Functions: getAllStudents, addStudent, updateStudentEmail, deleteStudent
# - Uses psycopg2 and environment variables for connection.
#
# Usage examples:
#   python app.py get_all
#   python app.py add --first "Ana" --last "Lopez" --email "ana.lopez@example.com" --date "2024-09-01"
#   python app.py update_email --id 1 --email "johnny.doe@example.com"
#   python app.py delete --id 3

import os
import argparse
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_conn():
    """
    Create and return a new database connection using environment variables.
    Expected env vars: PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
    """
    return psycopg2.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", "5432")),
        dbname=os.environ.get("PGDATABASE", "postgres"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD", "")
    )

def getAllStudents():
    """Retrieve and print all students from the table."""
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students ORDER BY student_id;")
        rows = cur.fetchall()
        if not rows:
            print("No students found.")
            return rows
        for r in rows:
            print(f"{r['student_id']:>3} | {r['first_name']} {r['last_name']} | {r['email']} | {r['enrollment_date']}")
        return rows

def addStudent(first_name, last_name, email, enrollment_date=None):
    """Insert a new student record."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s) RETURNING student_id;",
            (first_name, last_name, email, enrollment_date)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"Inserted student_id={new_id} for {first_name} {last_name}")
        return new_id

def updateStudentEmail(student_id, new_email):
    """Update email for a given student_id."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE students SET email = %s WHERE student_id = %s;", (new_email, student_id))
        if cur.rowcount == 0:
            print(f"No student found with id={student_id}")
        else:
            print(f"Updated email for student_id={student_id} -> {new_email}")
        conn.commit()

def deleteStudent(student_id):
    """Delete a student by student_id."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        if cur.rowcount == 0:
            print(f"No student found with id={student_id}")
        else:
            print(f"Deleted student_id={student_id}")
        conn.commit()

def main():
    parser = argparse.ArgumentParser(description="PostgreSQL CRUD for students table")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("get_all", help="List all students")

    add_p = sub.add_parser("add", help="Add a student")
    add_p.add_argument("--first", required=True, help="First name")
    add_p.add_argument("--last", required=True, help="Last name")
    add_p.add_argument("--email", required=True, help="Email (unique)")
    add_p.add_argument("--date", help="Enrollment date YYYY-MM-DD (optional)")

    upd_p = sub.add_parser("update_email", help="Update student email by id")
    upd_p.add_argument("--id", type=int, required=True, help="student_id")
    upd_p.add_argument("--email", required=True, help="New email")

    del_p = sub.add_parser("delete", help="Delete student by id")
    del_p.add_argument("--id", type=int, required=True, help="student_id")

    args = parser.parse_args()

    if args.cmd == "get_all":
        getAllStudents()
    elif args.cmd == "add":
        addStudent(args.first, args.last, args.email, args.date)
        getAllStudents()
    elif args.cmd == "update_email":
        updateStudentEmail(args.id, args.email)
        getAllStudents()
    elif args.cmd == "delete":
        deleteStudent(args.id)
        getAllStudents()

if __name__ == "__main__":
    main()