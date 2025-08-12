from flask import Flask, render_template, request, jsonify
from database import init_db, add_student, get_student

app = Flask(__name__)

# Tạo bảng khi chạy lần đầu
init_db()

@app.route('/')
def index():
    return render_template('index.html')

# API thêm sinh viên
@app.route('/add', methods=['POST'])
def add():
    ma_sv = request.form['ma_sv']
    ten_sv = request.form['ten_sv']
    lop = request.form['lop']
    nam_sinh = request.form['nam_sinh']

    add_student(ma_sv, ten_sv, lop, nam_sinh)
    return "Thêm sinh viên thành công!"

# API lấy sinh viên theo mã (cho App2 dùng)
@app.route('/api/student/<ma_sv>', methods=['GET'])
def api_get_student(ma_sv):
    student = get_student(ma_sv)
    if student:
        return jsonify({
            "id": student[0],
            "ma_sv": student[1],
            "ten_sv": student[2],
            "lop": student[3],
            "nam_sinh": str(student[4])
        })
    else:
        return jsonify({"error": "Không tìm thấy sinh viên"}), 404

if __name__ == '__main__':
    app.run(debug=True)
