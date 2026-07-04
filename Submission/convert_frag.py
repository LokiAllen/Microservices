import requests
import database
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from ENV.txt
load_dotenv("ENV.txt")

API_TOKEN = os.getenv("AUDD_KEY")
AUDD_URL = "https://api.audd.io/"

"""
This Endpoint is used to get an entire song and its information from a short segment of that song. Expects a POST request with form data
containing a file upload 'file' in .wav format.

Routes:
    Retrieves song information from the Audd.io API and checks if the song exists in the database. Returns the appropriate
    HTTP status codes based on the outcome:
        200 - OK (song found in the database, and returned to user)
        400 - Bad Request (missing or invalid data)
        404 - Not Found (song not found in the database)
        502 - Bad Gateway (error from Audd.io API)
"""
@app.route("/convert-song", methods=["POST"])
def convert_song_endpoint():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.wav'):
        file_path = file.filename
        file.save(file_path)
        
        files = {"file": open(file_path, "rb")}
        data = {"api_token": API_TOKEN}

        response = requests.post(AUDD_URL, files=files, data=data)
        result = response.json()

        if response.status_code != 200 or not result or result.get("status") != "success" or not result.get("result"):
            return "", 502 #Error from Audd.io

        # Extract song details
        song_title = result["result"].get("title", "Unknown Title")
        artist_name = result["result"].get("artist", "Unknown Artist")

        # Lookup the song in the database
        song_record = database.db.lookup(song_title, artist_name)

        if song_record:
            return jsonify(song_record), 200

        return "", 404  # The song is not in the database

    else:
        return "", 400 #File must be a .wav format

if __name__ == "__main__":
    app.run(host="localhost", port=3003)
