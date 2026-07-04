# test_setup.py
import database
import base64

def clear_database():
    """Utility function to clear the database before each test."""
    database.db.clear()

def open_audio_file(file_name):
    """Utility function to open an audio file in binary mode from the 'wavs' folder."""
    file_path = f'wavs/{file_name}'
    return open(file_path, 'rb')

def setup_database():
    """Setup function to clear the database and add 3 songs."""
    database.db.clear()

    songs = [
        {"name": "Blinding Lights", "artist": "The Weeknd", "file_name": "Blinding Lights.wav"},
        {"name": "Don't Look Back In Anger", "artist": "Oasis", "file_name": "Don't Look Back In Anger.wav"},
        {"name": "Everybody (Backstreet's Back) (Radio Edit)", "artist": "Backstreet Boys", "file_name": "Everybody (Backstreet's Back) (Radio Edit).wav"},
    ]

    for song in songs:
        with open_audio_file(song["file_name"]) as f:
            song_data = {
                "name": song["name"],
                "artist": song["artist"],
                "song": base64.b64encode(f.read()).decode('utf-8')  # Read and encode binary data to base64
            }
            database.db.insert(song_data)  # Insert into the database