import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=OCJ;"
    "Trusted_Connection=yes;" 
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

def get_testcases(problem_id):
    cursor.execute("""SELECT input_data,expected_output FROM
                 Testcases WHERE problem_id = ?
                 """, problem_id)
    result = cursor.fetchall()
    return result

def get_problem(problem_id):
    cursor.execute("""SELECT title, description, input_format, output_format, sample_input, sample_output FROM
                   Problems WHERE problem_id = ?
                   """, problem_id)
    result = cursor.fetchone()
    return result


def save_submission(problem_id, code_file, verdict):
    cursor.execute("""INSERT INTO Submissions
                   (problem_id, code, verdict)
                   VALUES (?, ?, ?)
                   """,problem_id, code_file, verdict)
    
    conn.commit()

def get_submissions(problem_id):
    cursor.execute("""SELECT submission_id, problem_id, verdict, submitted_at
                   FROM Submissions WHERE problem_id = ?
                   ORDER BY submission_id DESC
                   """, problem_id)
    
    result = cursor.fetchall()

    return result

def get_submission_by_id(submission_id):
    cursor.execute("""SELECT code
                   FROM Submissions WHERE submission_id = ?
                   """, submission_id)
    
    return cursor.fetchone()

def get_all_problems():
    cursor.execute("SELECT problem_id, title FROM Problems ORDER BY problem_id")
    return cursor.fetchall()
