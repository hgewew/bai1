import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import threading
import asyncio

# FastAPI app
app = FastAPI()

# Pydantic model for student data
class Student(BaseModel):
    name: str
    dob: str | None = None
    class_name: str | None = None

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Sinh Viên")
        self.root.geometry("800x600")

        # Kết nối cơ sở dữ liệu SQLite (giả lập SQL Server)
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Tạo giao diện
        self.create_widgets()

        # Chạy FastAPI server trong thread riêng
        self.start_api_server()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dob TEXT,
                class_name TEXT
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Frame nhập liệu
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Tên:").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Ngày sinh (YYYY-MM-DD):").grid(row=1, column=0, padx=5)
        self.dob_entry = tk.Entry(input_frame)
        self.dob_entry.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Lớp:").grid(row=2, column=0, padx=5)
        self.class_entry = tk.Entry(input_frame)
        self.class_entry.grid(row=2, column=1, padx=5)

        # Nút điều khiển
        tk.Button(input_frame, text="Thêm", command=self.add_student).grid(row=3, column=0, pady=10)
        tk.Button(input_frame, text="Sửa", command=self.update_student).grid(row=3, column=1, pady=10)
        tk.Button(input_frame, text="Xóa", command=self.delete_student).grid(row=3, column=2, pady=10)

        # Treeview hiển thị danh sách
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "DOB", "Class"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Tên")
        self.tree.heading("DOB", text="Ngày sinh")
        self.tree.heading("Class", text="Lớp")
        self.tree.pack(pady=10, fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.cursor.execute("SELECT * FROM Students")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def add_student(self):
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        class_name = self.class_entry.get()

        if not name:
            messagebox.showerror("Lỗi", "Tên không được để trống!")
            return

        try:
            if dob:
                datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày sinh phải là YYYY-MM-DD!")
            return

        self.cursor.execute("INSERT INTO Students (name, dob, class_name) VALUES (?, ?, ?)",
                          (name, dob, class_name))
        self.conn.commit()
        self.load_data()
        self.clear_entries()
        messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn một sinh viên để sửa!")
            return

        item = self.tree.item(selected[0])
        student_id = item["values"][0]
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        class_name = self.class_entry.get()

        if not name:
            messagebox.showerror("Lỗi", "Tên không được để trống!")
            return

        try:
            if dob:
                datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày sinh phải là YYYY-MM-DD!")
            return

        self.cursor.execute("UPDATE Students SET name = ?, dob = ?, class_name = ? WHERE id = ?",
                          (name, dob, class_name, student_id))
        self.conn.commit()
        self.load_data()
        self.clear_entries()
        messagebox.showinfo("Thành công", "Cập nhật sinh viên thành công!")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn một sinh viên để xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sinh viên này?"):
            item = self.tree.item(selected[0])
            student_id = item["values"][0]
            self.cursor.execute("DELETE FROM Students WHERE id = ?", (student_id,))
            self.conn.commit()
            self.load_data()
            self.clear_entries()
            messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]
            self.clear_entries()
            self.name_entry.insert(0, values[1])
            self.dob_entry.insert(0, values[2] if values[2] else "")
            self.class_entry.insert(0, values[3] if values[3] else "")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)

    def start_api_server(self):
        def run_server():
            uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
        # Chạy FastAPI trong thread riêng
        threading.Thread(target=run_server, daemon=True).start()

# FastAPI endpoints
@app.get("/students")
async def get_students():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    conn.close()
    return [{"id": s[0], "name": s[1], "dob": s[2], "class_name": s[3]} for s in students]

@app.post("/students")
async def add_student(student: Student):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    try:
        if student.dob:
            datetime.strptime(student.dob, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Định dạng ngày sinh phải là YYYY-MM-DD")
    
    if not student.name:
        raise HTTPException(status_code=400, detail="Tên không được để trống")
    
    cursor.execute("INSERT INTO Students (name, dob, class_name) VALUES (?, ?, ?)",
                  (student.name, student.dob, student.class_name))
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    return {"id": student_id, **student.dict()}

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")
    
    try:
        if student.dob:
            datetime.strptime(student.dob, "%Y-%m-%d")
    except ValueError:
        conn.close()
        raise HTTPException(status_code=400, detail="Định dạng ngày sinh phải là YYYY-MM-DD")
    
    if not student.name:
        conn.close()
        raise HTTPException(status_code=400, detail="Tên không được để trống")
    
    cursor.execute("UPDATE Students SET name = ?, dob = ?, class_name = ? WHERE id = ?",
                  (student.name, student.dob, student.class_name, student_id))
    conn.commit()
    conn.close()
    return {"id": student_id, **student.dict()}

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")
    
    cursor.execute("DELETE FROM Students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return {"message": "Xóa sinh viên thành công"}

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = StudentManagementApp(root)
    root.mainloop()