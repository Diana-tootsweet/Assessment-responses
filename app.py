import os
import json
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Submissions folder
SUBMISSIONS_FOLDER = "submissions"
if not os.path.exists(SUBMISSIONS_FOLDER):
    os.makedirs(SUBMISSIONS_FOLDER)

@app.route("/")
def index():
    return "Backend is running!"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json  # Capture the JSON data sent from the frontend

    # Validate the data
    if not data.get("name") or not data.get("email") or not data.get("edited_text"):
        return jsonify({"error": "Invalid data"}), 400

    # Generate a filename based on the timestamp and user's name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{data['name'].replace(' ', '_')}.json"
    filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

    # Save the data as a JSON file locally
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

    return jsonify({"message": "Response saved successfully!"}), 200

@app.route("/results", methods=["GET"])
def view_results():
    submissions = []
    # Loop through all files in the submissions folder
    for filename in os.listdir(SUBMISSIONS_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(SUBMISSIONS_FOLDER, filename)
            with open(filepath, "r") as file:
                submission = json.load(file)
                submission["file_name"] = filename  # Add the filename for reference
                submissions.append(submission)
    return jsonify(submissions)  # Return the submissions as JSON

@app.route("/results/html", methods=["GET"])
def view_results_html():
    submissions = []
    for filename in os.listdir(SUBMISSIONS_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(SUBMISSIONS_FOLDER, filename)
            with open(filepath, "r") as file:
                submission = json.load(file)
                submission["file_name"] = filename
                submissions.append(submission)
    return render_template("results.html", submissions=submissions)

if __name__ == "__main__":
    app.run(debug=True)
