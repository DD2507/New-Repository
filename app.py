from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

JENKINS_URL = "http://localhost:9090"
JOB_NAME = "auto-rollback-pipeline"
USERNAME = "dhrupad"
API_TOKEN = "1150c13ed47776caf8dd6aef02f2c008a7"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/trigger-update", methods=["POST"])
def trigger_update():

    build_url = f"{JENKINS_URL}/job/{JOB_NAME}/build"

    try:

        response = requests.post(
            build_url,
            auth=(USERNAME, API_TOKEN)
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code in [200, 201]:
            return jsonify({
                "status": "success",
                "message": "Jenkins pipeline triggered successfully"
            })

        return jsonify({
            "status": "failed",
            "message": f"Jenkins returned status {response.status_code}"
        }), 500

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "status": "failed",
            "message": str(e)
        }), 500

@app.route("/health")
def health():
    return "OK", 200

@app.route("/fail")
def fail():
    os._exit(1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)