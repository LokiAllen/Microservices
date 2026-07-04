import base64
import database
from flask import Flask, request, jsonify

app = Flask(__name__)

"""
This Endpoint is used to remove a song from the database. Expects a DELETE request with form data
containing 'name' and 'artist' which will uniquely identify the song.

Routes:
    Removes a song from the database if it exists. Returns the appropriate
    HTTP status codes based on the outcome:
        204 - Success with no content returned
        400 - Bad Request (missing or invalid data)
        404 - Conflict (song does not exist)
        500 - Internal Server Error (database deletion failed)
"""
@app.route("/remove-song", methods=["DELETE"])
def remove_song_endpoint():
    name = request.form.get("name")
    artist = request.form.get("artist")

    if not name or not artist:
        return "", 400  # Bad Request, Missing 'name' or 'artist' parameter

    song_record = {"name": name, "artist": artist}

    if database.db.lookup(name, artist) is None:
        return "", 404  # Song not found

    if database.db.delete(name, artist):
        return "", 204  # No Content
    else:
        return "", 500  # Internal Server Error, Failed to delete song

if __name__ == "__main__":
    app.run(host="localhost", port=3002)
