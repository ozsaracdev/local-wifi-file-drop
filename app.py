import os
import socket
import qrcode
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = "127.0.0.1"
    finally:
        s.close()
    return ip_address

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
    local_ip = get_local_ip()
    port = 5000
    server_url = f"http://{local_ip}:{port}"

    qr = qrcode.QRCode()
    qr.add_data(server_url)
    qr.make(fit=True)

    print("\n" + "=" * 45)
    print(f"Server running at: {server_url}")
    print("Scan this QR code with your phone camera:")
    print("=" * 45 + "\n")
    
    qr.print_ascii(invert=True)
    
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)