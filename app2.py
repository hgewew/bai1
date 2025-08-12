from flask import Flask, request, render_template
import requests

app = Flask(__name__)
API_URL = "http://localhost:5000/api/student/{}"  # API từ App 1

@app.route("/", methods=["GET", "POST"])
def index():
    student_data = None
    if request.method == "POST":
        ma_sv = request.form.get("ma_sv")
        if ma_sv:
            try:
                response = requests.get(API_URL.format(ma_sv))
                if response.status_code == 200:
                    student_data = response.json()
                else:
                    student_data = {"error": "Không tìm thấy sinh viên"}
            except Exception as e:
                student_data = {"error": f"Lỗi kết nối API: {str(e)}"}
    return render_template("index.html", student=student_data)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
