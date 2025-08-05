# bai1
Quản lý sinh viên
1. Giới thiệu
Dự án gồm 2 ứng dụng tkinter:
App1: Quản lý danh sách sinh viên, lưu trữ vào SQL Server và cung cấp API.
App2: Gọi API từ App1 để hiển thị danh sách sinh viên và thông tin chi tiết.
Cả hai ứng dụng giao tiếp qua HTTP API.
2. Công nghệ sử dụng và thuật toán
Ứng dụng quản lý sinh viên với API 
Ngôn ngữ lập trình:

Python: Ngôn ngữ chính được sử dụng để phát triển toàn bộ ứng dụng, do tính dễ đọc, linh hoạt và hỗ trợ mạnh mẽ cho giao diện người dùng, API, và kết nối cơ sở dữ liệu.

Công nghệ:

Tkinter: Thư viện chuẩn của Python để xây dựng giao diện đồ họa (GUI). Sử dụng để tạo các cửa sổ, ô nhập liệu, nút bấm và bảng hiển thị danh sách sinh viên.
FastAPI: Framework Python để xây dựng API RESTful. Được chọn vì hiệu suất cao (dựa trên Starlette và Pydantic) và hỗ trợ định nghĩa schema dữ liệu chặt chẽ.
SQLite: Cơ sở dữ liệu nhẹ được sử dụng để giả lập SQL Server trong môi trường Pyodide (do hạn chế kết nối mạng). Trong môi trường thực tế, có thể thay bằng SQL Server với thư viện pyodbc để kết nối.
Uvicorn: Server ASGI để chạy FastAPI, cho phép xử lý các yêu cầu HTTP đồng bộ và bất đồng bộ.
Pydantic: Được FastAPI sử dụng để định nghĩa và kiểm tra dữ liệu đầu vào (model Student) cho các endpoint API.
Threading: Sử dụng để chạy server FastAPI trong một luồng riêng, tránh chặn giao diện tkinter.

Thuật toán:

CRUD Operations: Ứng dụng thực hiện các thao tác cơ bản trên cơ sở dữ liệu:

Create: Thêm sinh viên mới (INSERT SQL).
Read: Lấy danh sách hoặc thông tin sinh viên (SELECT SQL).
Update: Cập nhật thông tin sinh viên (UPDATE SQL).
Delete: Xóa sinh viên (DELETE SQL).


Kiểm tra định dạng: Sử dụng datetime.strptime để kiểm tra định dạng ngày sinh (YYYY-MM-DD) trước khi thêm hoặc sửa.
Quản lý giao diện: Treeview của tkinter được dùng để hiển thị danh sách sinh viên, với thuật toán làm mới (refresh) dữ liệu bằng cách xóa và tái tạo các dòng trong bảng.
Xử lý bất đồng bộ: FastAPI sử dụng mô hình bất đồng bộ (async/await) để xử lý các yêu cầu HTTP hiệu quả.

2. Ứng dụng client gọi API (student_client.py)
Ngôn ngữ lập trình:

Python: Tương tự ứng dụng trước, Python được sử dụng để phát triển giao diện và gửi yêu cầu HTTP đến API.

Công nghệ:

Tkinter: Dùng để tạo giao diện người dùng tương tự ứng dụng quản lý, bao gồm ô nhập liệu, nút bấm và bảng hiển thị danh sách sinh viên.
Requests: Thư viện Python để gửi các yêu cầu HTTP (GET, POST, PUT, DELETE) tới API của ứng dụng quản lý sinh viên.
JSON: Định dạng dữ liệu được sử dụng để gửi và nhận thông tin qua API (ví dụ: gửi thông tin sinh viên dưới dạng JSON trong các yêu cầu POST/PUT).

Thuật toán:

Gọi API:

GET: Lấy danh sách sinh viên từ endpoint /students và hiển thị trong Treeview.
POST: Gửi dữ liệu sinh viên mới tới endpoint /students.
PUT: Cập nhật thông tin sinh viên tại endpoint /students/{id}.
DELETE: Xóa sinh viên tại endpoint /students/{id}.


Kiểm tra định dạng: Tương tự ứng dụng quản lý, kiểm tra định dạng ngày sinh (YYYY-MM-DD) và đảm bảo tên không để trống trước khi gửi yêu cầu API.
Xử lý lỗi: Xử lý các ngoại lệ HTTP (dùng response.raise_for_status()) và hiển thị thông báo lỗi qua messagebox nếu API trả về lỗi (ví dụ: 404, 400).
Quản lý giao diện: Tương tự ứng dụng quản lý, sử dụng Treeview để hiển thị danh sách và làm mới dữ liệu khi thực hiện các thao tác CRUD.
<img width="989" height="328" alt="image" src="https://github.com/user-attachments/assets/591b480a-f015-43f6-abc0-827a9e844dba" />
<img width="1748" height="349" alt="image" src="https://github.com/user-attachments/assets/02a44171-e804-471e-b786-0331fdf0f1a8" />
