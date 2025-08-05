import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý danh sách sinh viên")
        self.root.geometry("800x600")
        self.api_url = "http://172.16.12.138:8000"  # Địa chỉ API FastAPI

        # Kiểm tra kết nối API
        if not self.check_api_connection():
            self.root.destroy()
            return

        # Giao diện
        self.create_widgets()

    def check_api_connection(self):
        try:
            response = requests.get(f"{self.api_url}/students", timeout=5)
            response.raise_for_status()
            messagebox.showinfo("Thành công", "Kết nối tới API thành công!")
            return True
        except requests.exceptions.ConnectionError as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới server: {str(e)}\nKiểm tra API đang chạy.")
            return False
        except requests.exceptions.Timeout as e:
            messagebox.showerror("Lỗi kết nối", f"Timeout khi kết nối: {str(e)}\nKiểm tra mạng hoặc API.")
            return False
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Lỗi HTTP", f"Lỗi từ API: {str(e)}\nKiểm tra API hoặc cơ sở dữ liệu.")
            return False
        except Exception as e:
            messagebox.showerror("Lỗi không xác định", f"Lỗi: {str(e)}")
            return False

    def create_widgets(self):
        # Frame nhập liệu
        input_frame = ttk.LabelFrame(self.root, text="Thông tin sinh viên", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Các trường nhập liệu
        ttk.Label(input_frame, text="Họ tên:").grid(row=0, column=0, padx=5, pady=5)
        self.full_name = ttk.Entry(input_frame, width=30)
        self.full_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Lớp:").grid(row=1, column=0, padx=5, pady=5)
        self.class_name = ttk.Entry(input_frame, width=30)
        self.class_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Giới tính:").grid(row=2, column=0, padx=5, pady=5)
        self.gender = ttk.Combobox(input_frame, values=["Nam", "Nữ", "Khác"], width=27)
        self.gender.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Ngày sinh (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        self.birth_date = ttk.Entry(input_frame, width=30)
        self.birth_date.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Số điện thoại:").grid(row=4, column=0, padx=5, pady=5)
        self.phone_number = ttk.Entry(input_frame, width=30)
        self.phone_number.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Mã sinh viên:").grid(row=5, column=0, padx=5, pady=5)
        self.masinhvien = ttk.Entry(input_frame, width=30)
        self.masinhvien.grid(row=5, column=1, padx=5, pady=5)

        # Nút chức năng
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Thêm", command=self.add_student).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Sửa", command=self.update_student).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_student).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Làm mới", command=self.clear_fields).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Tải lại", command=self.load_data).grid(row=0, column=4, padx=5)

        # Treeview hiển thị danh sách
        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "Họ tên", "Lớp", "Giới tính", "Ngày sinh", "Số điện thoại", "Mã sinh viên"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Họ tên", text="Họ tên")
        self.tree.heading("Lớp", text="Lớp")
        self.tree.heading("Giới tính", text="Giới tính")
        self.tree.heading("Ngày sinh", text="Ngày sinh")
        self.tree.heading("Số điện thoại", text="Số điện thoại")
        self.tree.heading("Mã sinh viên", text="Mã sinh viên")
        self.tree.column("ID", width=50)
        self.tree.column("Họ tên", width=150)
        self.tree.column("Lớp", width=100)
        self.tree.column("Giới tính", width=80)
        self.tree.column("Ngày sinh", width=100)
        self.tree.column("Số điện thoại", width=100)
        self.tree.column("Mã sinh viên", width=100)
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.bind("<Double-1>", self.load_selected)

        # Thanh cuộn
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Tải dữ liệu ban đầu
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            response = requests.get(f"{self.api_url}/students", timeout=5)
            response.raise_for_status()
            students = response.json()
            for student in students:
                self.tree.insert("", "end", values=(
                    student["id"],
                    student["full_name"],
                    student["class_name"],
                    student["gender"],
                    student["birth_date"],
                    student["phone_number"] if student["phone_number"] else "",
                    student["masinhvien"] if student["masinhvien"] else ""
                ))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu từ API: {str(e)}")

    def add_student(self):
    # Lấy dữ liệu từ các input
        student_data = {
        "full_name": self.full_name.get(),
        "class_name": self.class_name.get(),
        "gender": self.gender.get(),
        "birth_date": self.birth_date.get(),
        "phone_number": self.phone_number.get(),
        "masinhvien": self.masinhvien.get()
        }

    # Kiểm tra dữ liệu bắt buộc
        for key in ["full_name", "class_name", "gender", "birth_date"]:
            if not student_data[key].strip():
                messagebox.showerror("Thiếu dữ liệu", f"{key} không được để trống!")
                return

    # Kiểm tra định dạng ngày sinh
        try:
            datetime.strptime(student_data["birth_date"], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Lỗi định dạng", "Ngày sinh phải đúng định dạng YYYY-MM-DD!")
            return

    # Gửi request tới API thêm sinh viên
        
        print("Gửi dữ liệu:", student_data)  # Debug
        response = requests.post("http://localhost:8000/students", json=student_data)
        if response.status_code in [200, 201]:
            data = response.json()
            messagebox.showinfo("Thành công", data.get("message", "Thêm sinh viên thành công!"))
            self.clear_inputs()
        else:
            messagebox.showerror("Lỗi", f"Lỗi từ server: {response.status_code}\n{response.text}")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sinh viên để sửa!")
            return

        try:
            item = self.tree.item(selected)
            student_id = item["values"][0]
            student_data = {
                "full_name": self.full_name.get(),
                "class_name": self.class_name.get(),
                "gender": self.gender.get(),
                "birth_date": self.birth_date.get(),
                "phone_number": self.phone_number.get() or None,
                "masinhvien": self.masinhvien.get() or None
            }
            if not all([student_data["full_name"], student_data["class_name"], student_data["gender"], student_data["birth_date"]]):
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ các trường bắt buộc!")
                return
            response = requests.put(f"{self.api_url}/students/{student_id}", json=student_data)
            response.raise_for_status()
            self.load_data()
            self.clear_fields()
            messagebox.showinfo("Thành công", "Cập nhật sinh viên thành công!")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật sinh viên: {str(e)}")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sinh viên để xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sinh viên này?"):
            try:
                item = self.tree.item(selected)
                student_id = item["values"][0]
                response = requests.delete(f"{self.api_url}/students/{student_id}")
                response.raise_for_status()
                self.load_data()
                self.clear_fields()
                messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Lỗi", f"Không thể xóa sinh viên: {str(e)}")

    def load_selected(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            values = item["values"]
            self.clear_fields()
            self.full_name.insert(0, values[1] if values[1] else "")
            self.class_name.insert(0, values[2] if values[2] else "")
            self.gender.set(values[3] if values[3] else "")
            self.birth_date.insert(0, values[4] if values[4] else "")
            self.phone_number.insert(0, values[5] if values[5] else "")
            self.masinhvien.insert(0, values[6] if values[6] else "")

    def clear_fields(self):
        self.full_name.delete(0, tk.END)
        self.class_name.delete(0, tk.END)
        self.gender.set("")
        self.birth_date.delete(0, tk.END)
        self.phone_number.delete(0, tk.END)
        self.masinhvien.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()