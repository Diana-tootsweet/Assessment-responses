import os
import json
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Submissions folder
SUBMISSIONS_FOLDER = "submissions"
if not os.path.exists(SUBMISSIONS_FOLDER):
    os.makedirs(SUBMISSIONS_FOLDER)

@app.route("/")
def index():
    submissions = []
    for file_name in os.listdir(SUBMISSIONS_FOLDER):
        if file_name.endswith(".json"):
            with open(os.path.join(SUBMISSIONS_FOLDER, file_name), "r") as file:
                data = json.load(file)
                submissions.append({
                    "name": data["name"],
                    "email": data["email"],
                    "timestamp": file_name.split(".json")[0],
                    "file_name": file_name
                })
    submissions.sort(key=lambda x: x["timestamp"], reverse=True)
    return render_template("index.html", submissions=submissions)

@app.route("/submission/<file_name>")
def view_submission(file_name):
    file_path = os.path.join(SUBMISSIONS_FOLDER, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        return render_template("submission.html", submission=data)
    else:
        return render_template("error.html", message="Submission not found."), 404

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json
        if not data.get("name") or not data.get("email") or not data.get("edited_text") or not data.get("time_spent"):
            return jsonify({"error": "Invalid data"}), 400

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_{data['name'].replace(' ', '_')}.json"
        filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Submission received: {data['name']} - {data['email']} at {timestamp}")
        return jsonify({"message": "Response saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run()
