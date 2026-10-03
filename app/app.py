
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "project": "AI-Powered Security Gate",
        "status": "running",
        "message": "Application is protected by the CI/CD security pipeline."
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
