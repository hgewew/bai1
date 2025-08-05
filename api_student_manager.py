from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
import pyodbc

app = FastAPI(title="Quản lý danh sách sinh viên API")

# ✅ Model dữ liệu sinh viên
class Student(BaseModel):
    id: Optional[int] = None
    full_name: str
    class_name: str         # mapping với cột SQL tên "class"
    gender: str
    birth_date: date        # cần có giá trị vì SQL NOT NULL
    phone_number: Optional[str] = None
    masinhvien: Optional[str] = None

# ✅ Hàm kết nối SQL Server
def get_db_connection():
    try:
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-L3PL7A87;'
            'DATABASE=danhsachsinhvien;'
            'Trusted_Connection=yes;'
        )
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Lỗi kết nối CSDL: {str(e)}")

# ✅ Lấy toàn bộ sinh viên
@app.get("/students", response_model=List[Student])
def get_all_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, full_name, class AS class_name, gender, birth_date, phone_number, masinhvien
            FROM Sinhvien
        """)
        return [
            Student(
                id=row[0], full_name=row[1], class_name=row[2], gender=row[3],
                birth_date=row[4], phone_number=row[5], masinhvien=row[6]
            ) for row in cursor.fetchall()
        ]
    finally:
        cursor.close()
        conn.close()

# ✅ Lấy sinh viên theo ID
@app.get("/students/{id}", response_model=Student)
def get_student(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, full_name, class AS class_name, gender, birth_date, phone_number, masinhvien
            FROM Sinhvien WHERE id = ?
        """, (id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Sinh viên không tìm thấy")
        return Student(
            id=row[0], full_name=row[1], class_name=row[2], gender=row[3],
            birth_date=row[4], phone_number=row[5], masinhvien=row[6]
        )
    finally:
        cursor.close()
        conn.close()

# ✅ Thêm sinh viên mới
@app.post("/students")
def create_student(student: Student):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Sinhvien (full_name, class, gender, birth_date, phone_number, masinhvien)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            student.full_name, student.class_name, student.gender,
            student.birth_date, student.phone_number, student.masinhvien
        ))
        conn.commit()
        return {"message": "Thêm sinh viên thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi thêm sinh viên: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# ✅ Cập nhật sinh viên theo ID
@app.put("/students/{id}")
def update_student(id: int, student: Student):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM Sinhvien WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
        cursor.execute("""
            UPDATE Sinhvien SET full_name = ?, class = ?, gender = ?, birth_date = ?, phone_number = ?, masinhvien = ?
            WHERE id = ?
        """, (
            student.full_name, student.class_name, student.gender,
            student.birth_date, student.phone_number, student.masinhvien, id
        ))
        conn.commit()
        return {"message": "Cập nhật sinh viên thành công"}
    finally:
        cursor.close()
        conn.close()

# ✅ Xóa sinh viên theo ID
@app.delete("/students/{id}")
def delete_student(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM Sinhvien WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
        cursor.execute("DELETE FROM Sinhvien WHERE id = ?", (id,))
        conn.commit()
        return {"message": "Xóa sinh viên thành công"}
    finally:
        cursor.close()
        conn.close()
