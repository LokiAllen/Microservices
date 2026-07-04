import requests
import unittest
import base64  # Import base64 for decoding
from test_setup import *
import json

convert_frag_url = "http://localhost:3003/convert-song"

class TestConvertFrag(unittest.TestCase):
    ###########################################################
    ## Test [1]: Convert Fragment and Inspect song_record    ##
    ###########################################################
    def test_convert_frag(self):
        setup_database()
        file_path = "~Everybody (Backstreet's Back) (Radio Edit).wav" 

        # Open the .wav file in binary mode
        with open_audio_file(file_path) as f:
            files = {
                "file": (file_path, f, "audio/wav")
            }

            # Send POST request to convert the fragment
            rsp = requests.post(convert_frag_url, files=files)

            # Check if the response status is 200 OK
            self.assertEqual(rsp.status_code, 200)

            # Verify the response contains song information
            response_data = rsp.json()

            self.assertEqual(response_data["name"], "Everybody (Backstreet's Back) (Radio Edit)")
            self.assertEqual(response_data["artist"], "Backstreet Boys")

            # Ensure the song data is present and correctly formatted
            self.assertIn("song", response_data)
            self.assertIsInstance(response_data["song"], str)  # Should be base64 string
            self.assertGreater(len(response_data["song"]), 0)

            # Attempt to decode the song from base64 to binary
            try:
                song_binary = base64.b64decode(response_data["song"])
                self.assertGreater(len(song_binary), 0)  # Ensure decoded binary data exists
            except base64.binascii.Error:
                self.fail("Failed to decode song data from base64")

    ###########################################################
    ## Test [2]: No File Provided                            ##
    ###########################################################
    def test_no_file_provided(self):
        clear_database()
        rsp = requests.post(convert_frag_url)

        # Check if the response status is 400 Bad Request
        self.assertEqual(rsp.status_code, 400)

    ###########################################################
    ## Test [3]: Invalid File Format                         ##
    ###########################################################
    def test_invalid_file_format(self):
        clear_database()
        file_path = "test.txt"  # Ensure this file is in the same directory

        # Open the .txt file in binary mode
        with open(file_path, 'rb') as f:
            files = {
                "file": (file_path, f, "text/plain")
            }

            # Send POST request to convert the fragment
            rsp = requests.post(convert_frag_url, files=files)

            # Check if the response status is 400 Bad Request
            self.assertEqual(rsp.status_code, 400)

    ###########################################################
    ## Test [4]: Invalid Song                                ##
    ###########################################################
    def test_invalid_song(self):
        clear_database()
        file_path = "~Davos.wav"

        # Open the .wav file in binary mode
        with open_audio_file(file_path) as f:
            files = {
                "file": (file_path, f, "audio/wav")
            }

            # Send POST request to convert the fragment
            rsp = requests.post(convert_frag_url, files=files)

            # Check if the response status is 502 Bad Gateway
            self.assertEqual(rsp.status_code, 502)


if __name__ == "__main__":
    unittest.main()
