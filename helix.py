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
    return requests.get(api + uri, headers=headers).json()


def search(**kwargs):
    """
    Full Doc Compatible See https://dev.twitch.tv/docs/api/reference/#get-streams

    :param kwargs:
    :return: Stream Info`s and PageKey
    """
    return call_api("streams?{0}".format(urlencode(kwargs))).json()


def search_vod():
    """ searches for VOD`s and returns an id for the VOD class """
    pass


def get_game(game_id=None, game_name=None):
    """
    Gets game info`s
    Only 1 Parameter Allowed, max 100 item per list, only one list

    :param game_name: a list of EXACT game names to query
    :type game_name: list
    :param game_id: a list of game id`s to query
    :type game_id: list
    :return: json containing the game data
    :rtype: list
    """
    identifier = None
    req = ''

    if game_id:
        identifier = 'id'

    if game_name:
        identifier = 'name'

    for e in game_name:
        tes = urlencode({identifier: str(e)})
        req = req + tes + '&'

    return call_api("games?{0}".format(req[:-1]))['data']


class Streamer:
    """A class containing the base Streamer info's
    Makes 1 call to the API and extracting the following Info's

    - .user_id: The User ID, whitley used in the API
    - .name: The capitalized Streamer Name
    - .url: twitch.tv/$name
    - .description: The Channel Description
    - .partner: The Partner Status
    - .profile_image_url: Url of the Profile Image
    - .offline_image_url: The Url to the Image that is shown if the Stream is Offline
    - .total_views: The Total amount of Views the Channel has
    """
    def __init__(self, name):
        # get basic info's for User
        user_data = call_api("users?login={0}".format(name))['data'][0]
        self.user_id = user_data['id']
        self.name = name
        self.url = 'twitch.tv/' + name
        self.description = user_data['description']
        self.partner = user_data['broadcaster_type']
        self.profile_image_url = user_data['profile_image_url']
        self.offline_image_url = user_data['offline_image_url']
        self.total_views = user_data['view_count']
        self.follows_page = ''
        self.follower_page = ''

    def follows(self, direction, total=False):
        """Iterates over the Users the Input is Following

        OR is Followed by
        in a Json object containing 100 users each Iteration.

        If Total is set to True returns the total followers as Type int instead.

        :param total: Default False. If True returns Total follows
        :type total: bool
        :param direction: Follow Direction "TO" Streamer "FROM" Streamer
        :type direction: str
        :returns: Follower Info`s OR None if Pool is empty
        :rtype: list
        """
        follows = None
        total_follows = None

        if (direction != 'TO') and (direction != 'FROM'):
            raise TypeError('Direction must be "TO" or "FROM"')

        if direction == 'TO':
            follows = call_api(
                "users/follows?from_id={0}&first=100&after={1}".format(self.user_id, self.follows_page))
            total_follows = follows['total']
            self.follows_page = follows['pagination']['cursor']

        if direction == 'FROM':
            follows = call_api(
                "users/follows?to_id={0}&first=100&after={1}".format(self.user_id, self.follower_page))
            total_follows = int(follows['total'])
            self.follower_page = follows['pagination']['cursor']

        if total is True:
            return total_follows

        try:
            if follows['pagination']['cursor']:
                pass
        except KeyError:
            return None

        del follows['pagination']
        return follows['data']

    def extensions(self):
        """Get the Active Extensions used by Streamer

        :returns: Streamers Active Extensions
        :rtype: list
        """
        extensions = call_api("users/extensions?user_id={0}".format(self.user_id))['data']

        e_index = []
        for e in extensions:
            for r in extensions[e]:
                if (extensions[e][r]['active']) == True:
                    del extensions[e][r]['active']
                    e_index.append({e: extensions[e][r]})
        return e_index

    # todo badges and emotes


class Vod(Streamer):
    """The vod Class"""

    def __init__(self, streamer):
        super(Vod, self).__init__(streamer)
        self.vod_data = call_api("videos?user_id={0}".format(self.user_id))


# class Clips(Streamer):
# def clips(self):
# todo make class for clips ?

#     """Get Clips"""
#     clips = call_api("clips?broadcaster_id={0}".format(self.user_id))
#     return clips['data']


class Stream(Streamer):
    """A Class that representing the base Stats of a Stream

    :param streamer: String with the url name of a streamer
    """
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
        streams = streamlink.streams(self.url)
        stream = streams[res].url
        return stream

    def get_tags(self):
        """Get the Tags of the Stream"""
        tags = call_api("streams/tags?broadcaster_id={0}".format(self.user_id))
        return tags['data']


# Aliases
get_games = get_game
