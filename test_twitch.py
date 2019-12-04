import unittest
from unittest.mock import patch, MagicMock

import twitch

mock_data = {'total': '23', 'data': [{'user_id': '123', 'broadcaster_id': '123', 'started_at': 'foo',
                                      'broadcaster_name': 'Gronkh', 'broadcaster_type': 'foo',
                                      'created_at': 'foo', 'profile_image_url': 'foo',
                                      'creator_id': '123', 'creator_name': 'foo', 'tag_ids': 'foo',
                                      'embed_url': 'foo', 'game_id': '123', 'duration': 'foo',
                                      'language': 'foo', 'thumbnail_url': 'foo', 'viewer_count': '123',
                                      'title': 'foo', 'url': 'foo', 'id': '123', 'type': 'foo',
                                      'video_id': '123', 'view_count': '123', 'user_name': 'Gronkh',
                                      'description': 'foo', 'published_at': 'foo', 'viewable': 'foo',
                                      'offline_image_url': 'foo'
                                      }], 'pagination': {'cursor': '12314'}}


class TestTwitchFunctions(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def test_call_api(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        # Good Request
        cm.read.return_value = b'{"data": [1, 2]}'
        test = twitch.call_api('streams?user_login=gronkh')
        self.assertEqual(test, {"data": [1, 2]})

        # Empty Answer
        cm.read.return_value = {"data": []}
        with self.assertRaises(Exception):
            twitch.call_api('streams?user_login=gronkh')

        # BAD Request
        cm.read.return_value = {"bar": "foo"}
        with self.assertRaises(Exception):
            twitch.call_api('streams?user_login=gronkh')

    @patch('twitch.call_api')
    def test_search(self, mocked_api):
        mocked_api.return_value = mock_data

        # test Stream
        test = twitch.search('Streams', user_login=['gronkh', 'lastmiles'], user_id=49112900)
        mocked_api.assert_called_with('streams?user_login=gronkh&user_login=lastmiles&user_id=49112900')
        # test response but i don't get it
        self.assertEqual(str(test)[:22], "[<twitch.Stream object")
        self.assertEqual(test[0].user_id, 123)
        self.assertEqual(test[0].name, 'Gronkh')
        self.assertEqual(test[0].stream_id, 123)
        self.assertEqual(test[0].game_id, 123)
        self.assertEqual(test[0].type, 'foo')
        self.assertEqual(test[0].title, 'foo')
        self.assertEqual(test[0].viewers, 123)
        self.assertEqual(test[0].started_at, 'foo')
        self.assertEqual(test[0].language, 'foo')
        self.assertEqual(test[0].thumbnail_url, 'foo')
        self.assertEqual(test[0].tag_ids, 'foo')

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

    @patch('twitch.call_api')
    def test_get_game(self, mocked_api):
        mocked_api.return_value = mock_data
        test = twitch.get_game(name=['Minecraft', 'League of Legends'], id=493057)
        mocked_api.assert_called_with('games?name=Minecraft&name=League+of+Legends&id=493057')
        self.assertEqual(test, mock_data['data'])

    @patch('twitch.call_api')
    def test_get_top_games(self, mocked_api):
        mocked_api.return_value = mock_data
        test = twitch.get_top_games(first=20)
        mocked_api.assert_called_with('games/top?first=20')
        self.assertEqual(test, mock_data['data'])


class TestStreamer(unittest.TestCase):
    @patch('twitch.call_api')
    def test_init(self, mocked_api):
        mocked_api.return_value = mock_data
        test = twitch.Streamer('Gronkh')
        mocked_api.assert_called_with('users?login=Gronkh')

        self.assertEqual(test.user_id, 123)
        self.assertEqual(test.name, 'Gronkh')
        self.assertEqual(test.url, 'twitch.tv/Gronkh')
        self.assertEqual(test.description, 'foo')
        self.assertEqual(test.partner, 'foo')
        self.assertEqual(test.profile_image_url, 'foo')
        self.assertEqual(test.offline_image_url, 'foo')
        self.assertEqual(test.total_views, 123)

    @patch('twitch.call_api')
    def test_extensions(self, mocked_api):
        mocked_api.return_value = mock_data

        test = twitch.Streamer('Gronkh')
        mocked_api.assert_called_with('users?login=Gronkh')

        mocked_api.return_value = {'data': {'panel': {'1': {'active': False},
                                                      '2': {'active': False},
                                                      '3': {'active': False}
                                                      },
                                            'overlay': {'1': {'active': True,
                                                              'id': 'c8okel68mmobvnso7ty0cygj8easam',
                                                              'version': '0.1.5',
                                                              'name': 'Smart Click Maps'}},
                                            'component': {'1': {'active': False},
                                                          '2': {'active': False}}}}

        self.assertEqual(test.extensions, {'overlay': {'id': 'c8okel68mmobvnso7ty0cygj8easam',
                                                       'name': 'Smart Click Maps',
                                                       'version': '0.1.5'}})

    @patch('twitch.call_api')
    def test_follower(self, mocked_api):
        mocked_api.return_value = mock_data
        test = twitch.Streamer('Gronkh')
        mocked_api.assert_called_with('users?login=Gronkh')
        self.assertEqual(test.follower, 23)

    @patch('twitch.call_api')
    def test_follows(self, mocked_api):
        # todo write a proper generator test
        mocked_api.return_value = mock_data
        test = twitch.Streamer('Phunk').follows('to')
        mocked_api.assert_called_with('users?login=Phunk')
        for e in test:
            self.assertEqual(e, mock_data['data'][0])

        mocked_api.return_value = mock_data
        test1 = twitch.Streamer('lastmiles').follows('from')
        mocked_api.assert_called_with('users?login=lastmiles')
        try:
            self.assertEqual(next(test1), mock_data['data'][0])
        except StopIteration:
            pass

        with self.assertRaises(ValueError):
            gen = twitch.Streamer('rw_grim').follows('hey')
            next(gen)


class TestStream(unittest.TestCase):
    @patch('twitch.call_api')
    def test_init(self, mocked_api):
        mocked_api.return_value = mock_data
        test = twitch.Stream('Gronkh')
        mocked_api.assert_called_with('streams?user_id=123')

        self.assertEqual(test.user_id, 123)
        self.assertEqual(test.name, 'Gronkh')
        self.assertEqual(test.url, 'twitch.tv/Gronkh')
        self.assertEqual(test.description, 'foo')
        self.assertEqual(test.partner, 'foo')
        self.assertEqual(test.profile_image_url, 'foo')
        self.assertEqual(test.offline_image_url, 'foo')
        self.assertEqual(test.total_views, 123)

    @patch('twitch.call_api')
    def test_get_tags(self, mocked_api):
        mocked_api.return_value = mock_data
        test = twitch.Stream('Gronkh').get_tags()
        mocked_api.assert_called_with('streams/tags?broadcaster_id=123')
        self.assertEqual(test, mock_data)


class TestVod(unittest.TestCase):
    @patch('twitch.call_api')
    def test_init(self, mocked_api):
        mocked_api.return_value = mock_data
        test = twitch.Vod(12345)
        mocked_api.assert_called_with('videos?id=12345')

        self.assertEqual(test.vod_id, 123)
        self.assertEqual(test.user_id, 123)
        self.assertEqual(test.name, 'Gronkh')
        self.assertEqual(test.url, 'foo')
        self.assertEqual(test.description, 'foo')
        self.assertEqual(test.created_at, 'foo')
        self.assertEqual(test.published_at, 'foo')
        self.assertEqual(test.thumbnail_url, 'foo')
        self.assertEqual(test.viewable, 'foo')
        self.assertEqual(test.view_count, 123)
        self.assertEqual(test.language, 'foo')
        self.assertEqual(test.type, 'foo')
        self.assertEqual(test.duration, 'foo')


class TestClip(unittest.TestCase):
    @patch('twitch.call_api')
    def test_init(self, mocked_api):
        mocked_api.return_value = mock_data
        test = twitch.Clip(12345)
        mocked_api.assert_called_with('clips?id=12345')

        self.assertEqual(test.clip_id, 12345)
        self.assertEqual(test.user_id, 123)
        self.assertEqual(test.name, 'Gronkh')
        self.assertEqual(test.url, 'foo')
        self.assertEqual(test.created_at, 'foo')
        self.assertEqual(test.creator_id, 123)
        self.assertEqual(test.creator_name, 'foo')
        self.assertEqual(test.embed_url, 'foo')
        self.assertEqual(test.game_id, 123)
        self.assertEqual(test.language, 'foo')
        self.assertEqual(test.thumbnail_url, 'foo')
        self.assertEqual(test.title, 'foo')
        self.assertEqual(test.url, 'foo')
        self.assertEqual(test.video_id, 123)
        self.assertEqual(test.view_count, 123)
