import base64
import database
from flask import Flask, request

app = Flask(__name__)

# Helper function to encode Base64
def encode_to_base64(file_content):
    return base64.b64encode(file_content).decode('utf-8')

"""
This Endpoint is used to add a song to the database. Expects a PUT request with form data
containing 'name', 'artist', and a file upload 'song' in .wav format.

Routes:
    Adds a song to the database if it does not already exist. Returns the appropriate
    HTTP status codes based on the outcome:
        201 - Created
        400 - Bad Request (missing or invalid data)
        409 - Conflict (song already exists)
        500 - Internal Server Error (database insertion failed)
"""
@app.route("/add-song", methods=["PUT"])
def add_song_endpoint():
    name = request.form.get("name")
    artist = request.form.get("artist")
    file = request.files.get("song")

    if name and artist and file:
        # Check if the file is a .wav
        if not file.filename.endswith('.wav'):
            return "", 400 #File must be a .wav format

        song_content = file.read()
        encoded_song = encode_to_base64(song_content)
        song_record = {"name": name, "artist": artist, "song": encoded_song}

        if database.db.lookup(name, artist) is not None:
            return "", 409  # Song already exists
        else:
            if database.db.insert(song_record):
                return "", 201  # Created
            else:
                return "", 500  # Internal Server Error
    else:
        return "", 400  # Bad Request

if __name__ == "__main__":
    app.run(host="localhost", port=3000)
