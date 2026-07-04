import requests
import unittest
import database
from test_setup import *

remove_song_url = "http://localhost:3002/remove-song"

class TestRemoveSong(unittest.TestCase):
    ###########################################################
    ## Test [1]: Remove Song                                 ##
    ###########################################################
    def test_remove_song(self):
        # Clear the database and add the songs before the test
        setup_database()

        # Test data
        name = "Don't Look Back In Anger"
        artist = "Oasis"

        # Send DELETE request to remove the song
        rsp = requests.delete(remove_song_url, data={"name": name, "artist": artist})

        # Check if the response status is 204 Created
        self.assertEqual(rsp.status_code, 204)

        # Verify the song is removed
        self.assertIsNone(database.db.lookup(name, artist))

    ###########################################################
    ## Test [2]: Remove a non existent song                  ##
    ###########################################################
    def test_remove_non_existent_song(self):
        # Clear the database and add songs before the test
        setup_database()

        # Test data
        name = "good 4 u"
        artist = "Olivia Rodrigo"

        # Send DELETE request to remove the song
        rsp = requests.delete(remove_song_url, data={"name": name, "artist": artist})

        self.assertEqual(rsp.status_code, 404)  # Conflict

    ###########################################################
    ## Test [2]: Invalid request                  ##
    ###########################################################
    def test_invalid_request(self):
        # Clear the database and add songs before the test
        setup_database()

        # provide only name
        name = "test name"

        # Send DELETE request to remove the song
        rsp = requests.delete(remove_song_url, data={"name": name})

        self.assertEqual(rsp.status_code, 400)  # Conflict

if __name__ == "__main__":
    unittest.main()
