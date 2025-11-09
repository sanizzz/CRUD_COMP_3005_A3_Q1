# PostgreSQL Students CRUD (Fast-Track)  video link to download is on brightspace

A tiny example that meets your assignment:

- SQL script to create the `students` table and seed rows
- Python app with 4 functions: `getAllStudents`, `addStudent`, `updateStudentEmail`, `deleteStudent`
- Steps for a quick demo video

## 0) Prereqs
- PostgreSQL 14+ (any recent is fine)
- Python 3.10+
- (Optional) pgAdmin for visual verification

## 1) Create database + table and seed data
Open a terminal and run psql against your target DB (or paste in pgAdmin):

```sql
-- Database setup script for 'students' table
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);

INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
```

> Tip: Re-run the script for a clean slate when recording.

## 2) Configure the app
Copy `.env.example` to `.env` and set your connection variables:
```
PGHOST=localhost
PGPORT=5432
PGDATABASE=YOUR_DB
PGUSER=YOUR_USER
PGPASSWORD=YOUR_PASS
```

## 3) Install dependencies
```
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## 4) Run the app (CRUD)
List all students:
```
python app.py get_all
```

Add a student:
```
python app.py add --first "Ana" --last "Lopez" --email "ana.lopez@example.com" --date "2024-09-01"
```

Update a student's email:
```
python app.py update_email --id 1 --email "johnny.doe@example.com"
```

Delete a student:
```
python app.py delete --id 3
```

Each command prints the table after the change so graders see the effect immediately.

## 5) Suggested video flow (≤ 5 min)
1. **Show pgAdmin**: Run the `db.sql` once; show table + seeded rows (John/Jane/Jim).
2. **Run `get_all`** in terminal.
3. **Run `add`** (Ana Lopez); show row appears in pgAdmin.
4. **Run `update_email`** (id=1); show updated email in pgAdmin.
5. **Run `delete`** (id=3); show deletion in pgAdmin.
6. Final `get_all` to show the end state.

## 6) Repo structure
```
pg-crud-students/
├─ app.py                # CRUD functions + CLI
├─ db.sql                # DDL + initial data
├─ requirements.txt
├─ .env.example
└─ README.md
```

## Notes for TAs
- Functions map 1:1 to rubric:
  - getAllStudents: SELECT list
  - addStudent: INSERT + RETURNING
  - updateStudentEmail: UPDATE by PK
  - deleteStudent: DELETE by PK
- Constraints: PK (serial), NOT NULLs, UNIQUE email, proper data types.
- Comments included in code and SQL.
