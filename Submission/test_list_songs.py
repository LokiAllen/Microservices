# test_list_songs.py
import requests
import unittest
from test_setup import *

get_songs_url = "http://localhost:3001/list-songs"

class TestListSongs(unittest.TestCase):
    ###########################################################
    ## Test [1]: List Songs                                  ##
    ###########################################################
    def test_list_songs(self):
        setup_database()

        setup_database()

        songs_to_check = [
            {"name": "Blinding Lights", "artist": "The Weeknd"},
            {"name": "Don't Look Back In Anger", "artist": "Oasis"},
            {"name": "Everybody (Backstreet's Back) (Radio Edit)", "artist": "Backstreet Boys"}
        ]

        rsp = requests.get(get_songs_url)
        self.assertEqual(rsp.status_code, 200)
        songs = rsp.json()
        for song in songs_to_check:
            self.assertTrue(any(s["name"] == song["name"] and s["artist"] == song["artist"] for s in songs))

    ###########################################################
    ## Test [2]: List Songs With Empty Database              ##
    ###########################################################
    def test_list_no_songss(self):
        clear_database()

        rsp = requests.get(get_songs_url)
        self.assertEqual(rsp.status_code, 200)
        songs = rsp.json()
        self.assertEqual(len(songs), 0)


if __name__ == "__main__":
    unittest.main()
