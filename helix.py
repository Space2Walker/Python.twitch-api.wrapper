#!/usr/bin/env python3
# author: Space2Walker
# 2019-10-18

from urllib.parse import urlencode

import requests
import streamlink

api = "https://api.twitch.tv/helix/"
headers = {'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}


def call_api(uri):
    """
    Call`s the Api https://api.twitch.tv/helix/uri
    :param uri: str
    :return: json object
    """
    response = requests.get(api + uri, headers=headers).json()
    # print(response.headers)
    return response


def search(**kwargs):
    """
    Full Doc Compatible See https://dev.twitch.tv/docs/api/reference/#get-streams
    :param kwargs:
    :return: Stream Info`s and PageKey
    """

    req = urlencode(kwargs)
    res = call_api("streams?{0}".format(req)).json()
    return res


def get_game(game_id):
    """
    Gets game info`s
    :param game_id: str
    :return: json containing the game data
    """
    game_data = call_api("games?id={0}".format(game_id))
    return game_data


def search_vod(self):
    """ searches for vods and returns an id for the vod class """
    pass


class Streamer:
    """docstring for Streamer"""

    def __init__(self, name):
        super(Streamer, self).__init__()
        self.name = name
        self.url = 'twitch.tv/' + name

        # get basic info's for User
        self.user_data = call_api("users?login={0}".format(self.name))

        self.user_id = self.user_data['data'][0]['id']
        self.description = self.user_data['data'][0]['description']
        self.partner = self.user_data['data'][0]['broadcaster_type']
        self.profile_image_url = self.user_data['data'][0]['profile_image_url']
        self.offline_image_url = self.user_data['data'][0]['offline_image_url']
        self.total_views = self.user_data['data'][0]['view_count']

    def follows(self, first=100, page=''):
        """Get the Users the Input is Following (Pagination)"""
        follows = call_api(
            "users/follows?from_id={0}&first={1}&after={2}".format(self.user_id, first, page))
        return follows

    def follower(self, first=20, page=''):
        """ Get the Users that Following the Input(Pagination)
        :param first: int: The Amount of followers per call max 200 default 20
        :param page: str: The Pagination key for next call
        :return: json: A Json object containing Follower Info`s
        """
        follower = call_api(
            "users/follows?to_id={0}&first={1}&after={2}".format(self.user_id, str(first), page))
        return follower

    def extensions(self):
        """Get the Extensions used in Stream"""
        extensions = call_api("users/extensions?user_id={0}".format(self.user_id))
        return extensions

    def clips(self):
        """Get Clips"""
        clips = call_api("clips?broadcaster_id={0}".format(self.user_id))
        return clips['data']


class Vod(Streamer):
    """The vod Class"""

    def __init__(self, streamer):
        super(Vod, self).__init__(streamer)
        self.vod_data = call_api("videos?user_id={0}".format(self.user_id))


class Stream(Streamer):
    def __init__(self, streamer):
        super(Stream, self).__init__(streamer)
        # get basic info`s of Stream
        self.stream_data = call_api("streams?user_id={0}".format(self.user_id))

        if self.stream_data['data']:
            self.stream_id = self.stream_data['data'][0]['id']
            self.game_id = self.stream_data['data'][0]['game_id']
            self.type = self.stream_data['data'][0]['type']
            self.title = self.stream_data['data'][0]['title']
            self.viewers = self.stream_data['data'][0]['viewer_count']
            self.started_at = self.stream_data['data'][0]['started_at']
            self.language = self.stream_data['data'][0]['language']
            self.thumbnail_url = self.stream_data['data'][0]['thumbnail_url']
            self.tag_ids = self.stream_data['data'][0]['tag_ids']
        else:
            self.stream_id = "offline"
            self.game_id = "offline"
            self.type = "offline"
            self.title = "offline"
            self.viewers = "offline"
            self.started_at = "offline"
            self.language = "offline"
            self.thumbnail_url = "offline"
            self.tag_ids = "offline"

    def get_hls(self, res='best'):
        """
        Crawls the HLS Url
        :param res: 720p, 1080p and so on
        :return: str: The HLS URL
        """
        self.streams = streamlink.streams(self.url)
        self.stream = self.streams[res].url
        return self.stream

    def get_tags(self):
        """Get the Tags of the Stream"""
        self.tags = call_api("streams/tags?broadcaster_id={0}".format(self.user_id))
        return self.tags['data']


# static-cdn.jtvnw.net/emoticons/v1/115390/1.0

k_api = "https://api.twitch.tv/kraken/"
k_headers = {'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}


def call_kraken(**kwargs):
    """
    Calls the Kraken API
    :type kwargs: dict: see twitch reference
    """
    req = urlencode(kwargs)
    response = requests.get(k_api + req, headers=k_headers)
    # print(response.headers)
    return response

# e_set = call_api('chat/emoticon_images?emotesets=19151')
