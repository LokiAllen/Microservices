import requests
import unittest
from test_setup import *

add_song_url = "http://localhost:3000/add-song"

class TestAddSong(unittest.TestCase):
    ###########################################################
    ## Test [1]: Add Song                                    ##
    ###########################################################
    def test_add_song(self):
        # Clear the database before the test
        clear_database()

        # Test data
        name = "good 4 u"
        artist = "Olivia Rodrigo"
        file_path = "good 4 u.wav"

        # Open the .wav file in binary mode
        with open_audio_file(file_path) as f:
            files = {
                "song": (file_path, f, "audio/wav")
            }
            data = {
                "name": name,
                "artist": artist
            }

            # Send PUT request to upload the song
            rsp = requests.put(add_song_url, data=data, files=files)

            # Check if the response status is 201 Created
            self.assertEqual(rsp.status_code, 201)

    ###########################################################
    ## Test [2]: Add Song Already in Database                ##
    ###########################################################
    def test_add_song_already_in_database(self):
        # Clear the database and add songs before the test
        setup_database()

        # Test data
        name = "Blinding Lights"
        artist = "The Weeknd"
        file_path = "Blinding Lights.wav"

        # Open the .wav file in binary mode
        with open_audio_file(file_path) as f:
            files = {
                "song": (file_path, f, "audio/wav")
            }
            data = {
                "name": name,
                "artist": artist
            }

            # Try to add a song that is already in the database
            rsp = requests.put(add_song_url, data=data, files=files)
            self.assertEqual(rsp.status_code, 409)  # Conflict

    ###########################################################
    ## Test [3]: Add Invalid File Format                     ##
    ###########################################################
    def test_add_invalid_file_format(self):
        # Clear the database before the test
        clear_database()

        # Test data
        name = "Invalid Song"
        artist = "Artist"
        file_path = "test.txt"

        # Open the .txt file in binary mode
        with open(file_path, 'rb') as f:
            files = {
                "song": (file_path, f, "text/plain")
            }
            data = {
                "name": name,
                "artist": artist
            }

            # Send PUT request to upload the song
            rsp = requests.put(add_song_url, data=data, files=files)

            # Check if the response status is 400 Bad Request
            self.assertEqual(rsp.status_code, 400)

if __name__ == "__main__":
    unittest.main()
