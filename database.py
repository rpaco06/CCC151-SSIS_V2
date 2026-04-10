import mysql.connector

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "your_password_here",
    "database": "ssis_v2"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ── Colleges ─────────────────────────────────────────────────
def load_colleges():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM college ORDER BY code")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def save_college(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO college (code, name) VALUES (%s, %s)",
        (data["code"], data["name"])
    )
    conn.commit()
    cursor.close()
    conn.close()

def update_college(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE college SET name=%s WHERE code=%s",
        (data["name"], data["code"])
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_college(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM college WHERE code=%s", (code,))
    conn.commit()
    cursor.close()
    conn.close()

def get_college_codes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM college ORDER BY code")
    codes = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return codes

def college_in_use(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM program WHERE college=%s", (code,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


# ── Programs ─────────────────────────────────────────────────
def load_programs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM program ORDER BY code")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def save_program(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO program (code, name, college) VALUES (%s, %s, %s)",
        (data["code"], data["name"], data["college"])
    )
    conn.commit()
    cursor.close()
    conn.close()

def update_program(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE program SET name=%s, college=%s WHERE code=%s",
        (data["name"], data["college"], data["code"])
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_program(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM program WHERE code=%s", (code,))
    conn.commit()
    cursor.close()
    conn.close()

def get_program_codes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM program ORDER BY code")
    codes = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return codes

def program_in_use(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM student WHERE course=%s", (code,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


# ── Students ─────────────────────────────────────────────────
def load_students(search="", sort="id", page=1, per_page=50):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    allowed_sort = ["id", "firstname", "lastname", "course", "year", "gender"]
    if sort not in allowed_sort:
        sort = "id"

    search_query = f"%{search}%"
    offset = (page - 1) * per_page

    cursor.execute(f"""
        SELECT * FROM student
        WHERE id LIKE %s
        OR firstname LIKE %s
        OR lastname LIKE %s
        OR course LIKE %s
        OR year LIKE %s
        OR gender LIKE %s
        ORDER BY {sort}
        LIMIT %s OFFSET %s
    """, (search_query, search_query, search_query,
          search_query, search_query, search_query,
          per_page, offset))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def count_students(search=""):
    conn = get_connection()
    cursor = conn.cursor()
    search_query = f"%{search}%"
    cursor.execute("""
        SELECT COUNT(*) FROM student
        WHERE id LIKE %s
        OR firstname LIKE %s
        OR lastname LIKE %s
        OR course LIKE %s
        OR year LIKE %s
        OR gender LIKE %s
    """, (search_query, search_query, search_query,
          search_query, search_query, search_query))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def save_student(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO student (id, firstname, lastname, course, year, gender) VALUES (%s, %s, %s, %s, %s, %s)",
        (data["id"], data["firstname"], data["lastname"],
         data["course"], data["year"], data["gender"])
    )
    conn.commit()
    cursor.close()
    conn.close()

def update_student(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE student SET firstname=%s, lastname=%s, course=%s, year=%s, gender=%s WHERE id=%s",
        (data["firstname"], data["lastname"], data["course"],
         data["year"], data["gender"], data["id"])
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_student(sid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE id=%s", (sid,))
    conn.commit()
    cursor.close()
    conn.close()

def student_exists(sid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM student WHERE id=%s", (sid,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0