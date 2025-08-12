import pyodbc

# ===== Thông tin kết nối SQL Server =====
SERVER = r"DESKTOP-J6G25L5\HGEWEW"   # Sửa thành tên instance SQL Server của bạn
DATABASE = "StudentApp"
USERNAME = "sa"
PASSWORD = "sa"

def get_connection():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD}"
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Students' AND xtype='U')
        CREATE TABLE Students (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ma_sv NVARCHAR(50) NOT NULL,
            ten_sv NVARCHAR(200) NOT NULL,
            lop NVARCHAR(50),
            nam_sinh DATE
        )
    """)
    conn.commit()
    conn.close()

def add_student(ma_sv, ten_sv, lop, nam_sinh):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Students (ma_sv, ten_sv, lop, nam_sinh)
            VALUES (?, ?, ?, ?)
        """, (ma_sv, ten_sv, lop, nam_sinh))
        conn.commit()
    except Exception as e:
        print("Lỗi khi thêm sinh viên:", e)
    finally:
        conn.close()

def get_student(ma_sv):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, ma_sv, ten_sv, lop, nam_sinh FROM Students WHERE ma_sv = ?", (ma_sv,))
    row = cursor.fetchone()
    conn.close()
    return row
