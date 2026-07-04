import base64
import database
from flask import Flask, request

app = Flask(__name__)

# Helper function to decode Base64
def decode_from_base64(encoded_content):
    return base64.b64decode(encoded_content)

"""
This Endpoint is used to list all songs from the database. Expects a GET request with no parameters.

Routes:
    Gets a list of songs from the database. Returns the appropriate
    HTTP status codes based on the outcome:
        200 - Success with list of songs returned
        404 - Conflict (database is empty)
"""
@app.route("/list-songs", methods=["GET"])
def list_songs_endpoint():
    songs = database.db.return_all()
    if songs is not None:
        filtered_songs = [{"name": song["name"], "artist": song["artist"]} for song in songs]
        return filtered_songs, 200  # OK
    else:
        return "", 404  # Not Found

if __name__ == "__main__":
    app.run(host="localhost", port=3001)



    