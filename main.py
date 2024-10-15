from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    subprocess.call(["python", "script.py"])  # Replace with the actual script link
    return "Script running successfully!"

if __name__ == "__main__":
    app.run(debug=True)
