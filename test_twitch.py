import unittest
from unittest.mock import patch

import twitch

mock_data = [{'user_id': 'foo', 'broadcaster_id': 'foo', 'started_at': 'foo',
              'broadcaster_name': 'foo', 'created_at': 'foo',
              'creator_id': 'foo', 'creator_name': 'foo', 'tag_ids': 'foo',
              'embed_url': 'foo', 'game_id': 'foo', 'duration': 'foo',
              'language': 'foo', 'thumbnail_url': 'foo', 'viewer_count': 'foo',
              'title': 'foo', 'url': 'foo', 'id': 'foo', 'type': 'foo',
              'video_id': 'foo', 'view_count': 'foo', 'user_name': 'foo',
              'description': 'foo', 'published_at': 'foo', 'viewable': 'foo'
              }]


class TestTwitch(unittest.TestCase):
    def test_call_api(self):
        with patch('requests.get') as mocked_get:
            # GOOD Request
            mocked_get.return_value.json.return_value = {"data": "foo"}
            # test request parameter
            test = twitch.call_api('streams?user_login=gronkh')
            mocked_get.assert_called_with((twitch.api + 'streams?user_login=gronkh'), headers=twitch.headers)
            # test response
            self.assertEqual(str(test), "foo")

            # BAD Request
            mocked_get.return_value.json.return_value = {"bar": "foo"}
            with self.assertRaises(Exception):
                twitch.call_api('streams?user_login=gronkh')

    def test_search(self):
        with patch('twitch.call_api') as mocked_api:
            mocked_api.return_value = mock_data

            # test Stream
            test = twitch.search('Streams', user_login=['gronkh', 'lastmiles'], user_id=49112900)
            mocked_api.assert_called_with('streams?user_login=gronkh&user_login=lastmiles&user_id=49112900')
            # test response but i don't get it
            self.assertEqual(str(test)[:22], "[<twitch.Stream object")

            # test Vod
            test = twitch.search("VIDEOS", user_login=['gronkh', 'lastmiles'], user_id=49112900)
            mocked_api.assert_called_with('videos?user_login=gronkh&user_login=lastmiles&user_id=49112900')
            # test response but i don't get it
            self.assertEqual(str(test)[:19], "[<twitch.Vod object")

            # test Clip
            test = twitch.search("CLIPS", user_login=['gronkh', 'lastmiles'], user_id=49112900)
            mocked_api.assert_called_with('clips?user_login=gronkh&user_login=lastmiles&broadcaster_id=49112900')
            # test response but i don't get it
            self.assertEqual(str(test)[:20], "[<twitch.Clip object")

    def test_get_game(self):
        with patch('twitch.call_api') as mocked_api:
            mocked_api.return_value = mock_data
            test = twitch.get_game(name=['Minecraft', 'League of Legends'], id=493057)
            mocked_api.assert_called_with('games?name=Minecraft&name=League+of+Legends&id=493057')
            self.assertEqual(test, mock_data)

    def test_get_top_games(self):
        with patch('twitch.call_api') as mocked_api:
            mocked_api.return_value = mock_data
            test = twitch.get_top_games(first=20)
            mocked_api.assert_called_with('games/top?first=20')
            self.assertEqual(test, mock_data)


if __name__ == '__main__':
    unittest.main()
