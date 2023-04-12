from flask import Flask, Response
import cv2

app = Flask(__name__)

# Replace the values in angle brackets with your own information
username = "admin"
password = "gzrobot123"
ip_address = "10.89.36.75"
port = "2554"
stream_path = ""
rtsp_url = f"rtsp://{username}:{password}@{ip_address}:{port}/{stream_path}"

cap = cv2.VideoCapture(rtsp_url)

def gen_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)