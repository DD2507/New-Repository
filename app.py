from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Version 1: Application Running Successfully!"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/fail")
def fail():
    os._exit(1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)