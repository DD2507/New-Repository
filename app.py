from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
import requests
import os
load_dotenv()

app = Flask(__name__)

JENKINS_URL = "http://localhost:9090"
JOB_NAME = "auto-rollback-pipeline"
USERNAME = "dhrupad"
API_TOKEN = os.getenv("JENKINS_API_TOKEN")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/trigger-update", methods=["POST"])
def trigger_update():

    build_url = f"{JENKINS_URL}/job/{JOB_NAME}/build"

    try:

        # Trigger Jenkins build
        response = requests.post(
            build_url,
            auth=(USERNAME, API_TOKEN)
        )

        if response.status_code not in [200, 201]:
            return jsonify({
                "status": "failed",
                "message": "Failed to trigger Jenkins"
            }), 500

        import time

        # Wait for Jenkins to start build
        time.sleep(5)

        # Get latest build info
        api_url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/api/json"

        while True:

            build_info = requests.get(
                api_url,
                auth=(USERNAME, API_TOKEN)
            ).json()

            building = build_info["building"]

            if not building:
                break

            time.sleep(3)

        result = build_info["result"]

        if result == "SUCCESS":

            return jsonify({
                "status": "success",
                "message": "Deployment Successful"
            })

        else:

            return jsonify({
                "status": "failed",
                "message": "Deployment Failed - Rollback Triggered"
            })

    except Exception as e:

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