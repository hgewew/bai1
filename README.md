# bai1
Quản lý sinh viên
1. Giới thiệu
Bài làm gồm 2 ứng dụng web (App 1 và App 2) tương tác với nhau thông qua API để quản lý và tra cứu thông tin sinh viên:
App 1: Cho phép nhập và lưu danh sách sinh viên vào cơ sở dữ liệu SQL Server, đồng thời cung cấp API để lấy thông tin sinh viên theo mã.
App 2: Gọi API từ App 1 và hiển thị thông tin sinh viên ra giao diện web khi người dùng nhập mã.
2. Công nghệ sử dụng và thuật toán
Ứng dụng quản lý sinh viên với API 
Ngôn ngữ lập trình
Python 3.x — dùng để xây dựng ứng dụng backend với Flask.
Công nghệ & Thư viện
Flask (Python) — tạo web server và API.
PyODBC — thư viện kết nối Python với SQL Server.
Bootstrap 5 — CSS framework để tạo giao diện đẹp, responsive.
Fetch API (JavaScript) — gọi API từ App 2 tới App 1.
Cơ sở dữ liệu
SQL Server 2022 — lưu trữ thông tin sinh viên.
Kiểu kết nối
ODBC Driver 17 for SQL Server — driver kết nối Python với SQL Server.
REST API — App 1 trả dữ liệu JSON cho App 2 qua HTTP.
Thuật toán
Không sử dụng thuật toán phức tạp, chủ yếu là:
CRUD cơ bản (Create, Read) trên SQL Server.
Xử lý request-response giữa client và server qua API.

Hiển thị dữ liệu dưới dạng bảng HTML.
<img width="1646" height="706" alt="image" src="https://github.com/user-attachments/assets/0bfdf8b3-e0bc-407f-9790-df1fa2c0b7c7" />
<img width="1623" height="222" alt="image" src="https://github.com/user-attachments/assets/2d2a4630-825e-4620-86c7-0d15813eda1a" />

