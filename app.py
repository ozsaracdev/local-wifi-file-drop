import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    status_message = None

    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename != "":
            target_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(target_path)
            status_message = f"'{uploaded_file.filename}' uploaded successfully!"

    file_list = os.listdir(UPLOAD_FOLDER)

    return render_template("index.html", message=status_message, files=file_list)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)