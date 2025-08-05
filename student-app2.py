import tkinter as tk
from tkinter import messagebox, ttk
import requests
from datetime import datetime

class StudentClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Gọi API Quản Lý Sinh Viên")
        self.root.geometry("800x600")
        self.api_base_url = "http://localhost:8000"

        # Tạo giao diện
        self.create_widgets()

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
        tk.Button(input_frame, text="Lấy Danh Sách", command=self.get_students).grid(row=3, column=0, pady=10)
        tk.Button(input_frame, text="Thêm", command=self.add_student).grid(row=3, column=1, pady=10)
        tk.Button(input_frame, text="Sửa", command=self.update_student).grid(row=3, column=2, pady=10)
        tk.Button(input_frame, text="Xóa", command=self.delete_student).grid(row=3, column=3, pady=10)

        # Treeview hiển thị danh sách
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "DOB", "Class"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Tên")
        self.tree.heading("DOB", text="Ngày sinh")
        self.tree.heading("Class", text="Lớp")
        self.tree.pack(pady=10, fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def get_students(self):
        try:
            response = requests.get(f"{self.api_base_url}/students")
            response.raise_for_status()
            students = response.json()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for student in students:
                self.tree.insert("", "end", values=(
                    student["id"],
                    student["name"],
                    student["dob"] if student["dob"] else "",
                    student["class_name"] if student["class_name"] else ""
                ))
        except requests.RequestException as e:
            messagebox.showerror("Lỗi", f"Không thể lấy danh sách sinh viên: {str(e)}")

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

        data = {"name": name, "dob": dob if dob else None, "class_name": class_name if class_name else None}
        try:
            response = requests.post(f"{self.api_base_url}/students", json=data)
            response.raise_for_status()
            self.get_students()
            self.clear_entries()
            messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
        except requests.RequestException as e:
            messagebox.showerror("Lỗi", f"Không thể thêm sinh viên: {str(e)}")

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

        data = {"name": name, "dob": dob if dob else None, "class_name": class_name if class_name else None}
        try:
            response = requests.put(f"{self.api_base_url}/students/{student_id}", json=data)
            response.raise_for_status()
            self.get_students()
            self.clear_entries()
            messagebox.showinfo("Thành công", "Cập nhật sinh viên thành công!")
        except requests.RequestException as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật sinh viên: {str(e)}")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn một sinh viên để xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sinh viên này?"):
            item = self.tree.item(selected[0])
            student_id = item["values"][0]
            try:
                response = requests.delete(f"{self.api_base_url}/students/{student_id}")
                response.raise_for_status()
                self.get_students()
                self.clear_entries()
                messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
            except requests.RequestException as e:
                messagebox.showerror("Lỗi", f"Không thể xóa sinh viên: {str(e)}")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentClientApp(root)
    root.mainloop()