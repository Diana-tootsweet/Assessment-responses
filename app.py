import os
import json
from flask import Flask, jsonify, render_template, request
from datetime import datetime

app = Flask(__name__)

# Submissions folder
SUBMISSIONS_FOLDER = "submissions"
if not os.path.exists(SUBMISSIONS_FOLDER):
    os.makedirs(SUBMISSIONS_FOLDER)

@app.route("/")
def index():
    # Fetch all submissions
    submissions = []
    for file_name in os.listdir(SUBMISSIONS_FOLDER):
        if file_name.endswith(".json"):
            with open(os.path.join(SUBMISSIONS_FOLDER, file_name), "r") as file:
                data = json.load(file)
                submissions.append({
                    "name": data["name"],
                    "email": data["email"],
                    "timestamp": file_name.split(".")[0],  # Extract timestamp from filename
                    "file_name": file_name  # Include filename for link
                })

    # Sort submissions by date/time
    submissions.sort(key=lambda x: x["timestamp"], reverse=True)

    # Render the list of submissions
    return render_template("index.html", submissions=submissions)

@app.route("/submission/<file_name>")
def view_submission(file_name):
    # Load the specific submission file
    file_path = os.path.join(SUBMISSIONS_FOLDER, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        return render_template("submission.html", submission=data)
    else:
        return "Submission not found", 404

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    # Validate the data
    if not data.get("name") or not data.get("email") or not data.get("edited_text") or not data.get("time_spent"):
        return jsonify({"error": "Invalid data"}), 400

    # Generate a filename based on timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{data['name'].replace(' ', '_')}.json"
    filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

    # Save the data as a JSON file
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

    return jsonify({"message": "Response saved successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
