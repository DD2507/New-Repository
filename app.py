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

    try:

        import time

        # Get next build number
        info_url = f"{JENKINS_URL}/job/{JOB_NAME}/api/json"

        job_info_response = requests.get(
            info_url,
            auth=(USERNAME, API_TOKEN)
        )

        job_info = job_info_response.json()

        build_number = job_info["nextBuildNumber"]

        # Trigger build
        build_url = f"{JENKINS_URL}/job/{JOB_NAME}/build"

        response = requests.post(
            build_url,
            auth=(USERNAME, API_TOKEN)
        )

        if response.status_code not in [200, 201]:
            return jsonify({
                "status": "failed",
                "message": "Failed to trigger Jenkins"
            }), 500

        # Wait for Jenkins to create build
        time.sleep(10)

        build_api = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/api/json"

        while True:

            build_response = requests.get(
                build_api,
                auth=(USERNAME, API_TOKEN)
            )

            # Jenkins may not have build ready yet
            if build_response.status_code != 200:
                time.sleep(3)
                continue

            try:
                build_info = build_response.json()
            except:
                time.sleep(3)
                continue

            # Wait until build completes
            if not build_info.get("building", False):
                break

            time.sleep(3)

        result = build_info.get("result", "FAILURE")

        print("BUILD RESULT:", result)

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