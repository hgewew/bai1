import requests
import tkinter as tk
from tkinter import ttk, messagebox

API_URL = "http://172.16.12.138:8000/students"

def load_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        for row in tree.get_children():
            tree.delete(row)

        for student in data:
            tree.insert('', 'end', values=(
                student['id'],
                student['full_name'],
                student['class_name'],
                student['gender'],
                student['birth_date'],
                student['phone_number'],
                student['masinhvien']
            ))
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

root = tk.Tk()
root.title("Danh sách sinh viên")

columns = ('ID', 'Họ và tên', 'Lớp', 'Giới tính', 'Ngày sinh', 'SĐT', 'Mã SV')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill='both', expand=True)

btn = ttk.Button(root, text="Tải danh sách", command=load_data)
btn.pack(pady=10)

root.mainloop()
