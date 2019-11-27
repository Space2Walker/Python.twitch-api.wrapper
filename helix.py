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
    Call`s the Api https://api.twitch.tv/helix/$uri

    :param uri: str
    :return: json object
    """
    # todo implement error handling and rate limiting
    return requests.get(api + uri, headers=headers).json()


def search(identifier, **kwargs):
    """
    Full Doc Compatible See
    https://dev.twitch.tv/docs/api/reference/#get-streams
    https://dev.twitch.tv/docs/api/reference/#get-videos
    https://dev.twitch.tv/docs/api/reference/#get-clips

    :param identifier: 'STREAMS' OR 'VIDEOS' OR 'CLIP'
    :param kwargs: user_login=['gronkh', 'lastmiles'], user_id=[49112900]
    :return: Stream Class Object or list of Objects
    :rtype: collections.defaultlist or Stream
    """
    req = ''
    ret = []

    # stick to your naming convention twitch for god sake
    if identifier.upper() == 'CLIPS':
        # renames the dict Key
        kwargs['broadcaster_id'] = kwargs.pop('user_id')

    # get the kwargs keys and iterate
    for e in kwargs.keys():
        ''' goes over the list of values per key and makes a string 
        user_login=gronkh&user_login=lastmiles&user_id=49112900&
        where user_login is the key and "gronkh" and "lastmiles" are the values in the list of that key
        '''
        for val in kwargs[e]:
            tes = urlencode({e: str(val)})
            req = req + tes + '&'

    res = call_api(f"{identifier.lower()}?{req[:-1]}")['data']

    try:
        test = res[0]
    except IndexError:
        raise Exception("NO DATA Your request didn't get any data back")

    if identifier.upper() == 'STREAMS':
        for e in res:
            ret.append(Stream(e['user_name'], self_init=False, **e))
        return ret

    if identifier.upper() == 'VIDEOS':
        for e in res:
            ret.append(Vod(e['id'], self_init=False, **e))
        return ret

    if identifier.upper() == 'CLIPS':
        for e in res:
            ret.append(Clip(e['broadcaster_id'], self_init=False, **e))
        return ret


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


def get_hls(url, res='best'):
    """
    Crawls the HLS Url
    :param url: The Twitch video or Stream Url
    :param res: 720p, 1080p and so on
    :return: str: The HLS URL
    """
    streams = streamlink.streams(url)
    stream = streams[res].url
    return stream


# todo top games method https://dev.twitch.tv/docs/api/reference#get-top-games


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
            try:
                self.follows_page = follows['pagination']['cursor']
            except KeyError:
                return None

        if direction == 'FROM':
            follows = call_api(
                "users/follows?to_id={0}&first=100&after={1}".format(self.user_id, self.follower_page))
            total_follows = int(follows['total'])
            try:
                self.follower_page = follows['pagination']['cursor']
            except KeyError:
                return None

        if total is True:
            return total_follows

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
                if extensions[e][r]['active']:
                    del extensions[e][r]['active']
                    e_index.append({e: extensions[e][r]})
        return e_index

    # todo badges and emotes


class Stream(Streamer):
    """A Class that representing the base Stats of a Stream"""

    def __init__(self, streamer, self_init=True, **kwargs):
        if self_init:
            super(Stream, self).__init__(streamer)
            # get basic info`s of Stream
            self.stream_data = call_api("streams?user_id={0}".format(self.user_id))['data']

            try:
                self.stream_id = self.stream_data[0]['id']
                self.game_id = self.stream_data[0]['game_id']
                self.type = self.stream_data[0]['type']
                self.title = self.stream_data[0]['title']
                self.viewers = self.stream_data[0]['viewer_count']
                self.started_at = self.stream_data[0]['started_at']
                self.language = self.stream_data[0]['language']
                self.thumbnail_url = self.stream_data[0]['thumbnail_url']
                self.tag_ids = self.stream_data[0]['tag_ids']

            except IndexError:
                self.type = "offline"

        if not self_init:
            self.user_id = kwargs['user_id']
            self.user_name = kwargs['user_name']
            self.stream_id = kwargs['id']
            self.game_id = kwargs['game_id']
            self.type = kwargs['type']
            self.title = kwargs['title']
            self.viewers = kwargs['viewer_count']
            self.started_at = kwargs['started_at']
            self.language = kwargs['language']
            self.thumbnail_url = kwargs['thumbnail_url']
            self.tag_ids = kwargs['tag_ids']

    def get_tags(self):
        """Get the Tags of the Stream"""
        tags = call_api("streams/tags?broadcaster_id={0}".format(self.user_id))
        return tags['data']

    # todo get_meta https://dev.twitch.tv/docs/api/reference#get-streams-metadata
    # uses its one rate limiting


class Vod:
    # todo optional inherit from Streamer
    """The vod Class

    - .vod_id: The VOD ID
    - .user_id: The User ID, whitley used in the API
    - .user_name: The capitalized Streamer Name
    - .url: twitch.tv/videos/vod_id
    - .title: The Stream Title
    - .description: The VOD Description
    - .created_at: Time the Vod was created
    - .published_at: Time the Vod was published
    - .thumbnail_url: Url of the Vod Thumbnail
    - .viewable: is Public viewable or not
    - .view_count: The view count of the VOD
    - .language: The language the vod is in
    - .type: Type of video. Valid values: "upload", "archive", "highlight".
    - .duration: the duration of the Vod
    """

    def __init__(self, vod_id, self_init=True, **kwargs):
        if self_init:
            self.vod_data = call_api("videos?id={0}".format(vod_id))['data'][0]

            self.vod_id = self.vod_data['id']
            self.user_id = self.vod_data['user_id']
            self.user_name = self.vod_data['user_name']
            self.url = self.vod_data['url']
            self.title = self.vod_data['title']
            self.description = self.vod_data['description']
            self.created_at = self.vod_data['created_at']
            self.published_at = self.vod_data['published_at']
            self.thumbnail_url = self.vod_data['thumbnail_url']
            self.viewable = self.vod_data['viewable']
            self.view_count = self.vod_data['view_count']
            self.language = self.vod_data['language']
            self.type = self.vod_data['type']
            self.duration = self.vod_data['duration']

        if not self_init:
            self.vod_id = vod_id
            self.user_id = kwargs['user_id']
            self.user_name = kwargs['user_name']
            self.url = kwargs['url']
            self.title = kwargs['title']
            self.description = kwargs['description']
            self.created_at = kwargs['created_at']
            self.published_at = kwargs['published_at']
            self.thumbnail_url = kwargs['thumbnail_url']
            self.viewable = kwargs['viewable']
            self.view_count = kwargs['view_count']
            self.language = kwargs['language']
            self.type = kwargs['type']
            self.duration = kwargs['duration']


class Clip:
    # todo optional inherit from Streamer
    """ The Clip Class

    .user_id        User ID of the stream from which the clip was created.
    .user_name      Display name corresponding to user_id.
    .created_at     Date when the clip was created.
    .creator_id	    ID of the user who created the clip.
    .creator_name   Display name corresponding to creator_id.
    .embed_url      URL to embed the clip.
    .game_id        ID of the game assigned to the stream when the clip was created.
    .id	            ID of the clip being queried.
    .language       Language of the stream from which the clip was created.
    .thumbnail_url	string	URL of the clip thumbnail.
    .title          Title of the clip.
    .url            URL where the clip can be viewed.
    .video_id       ID of the video from which the clip was created.
    .view_count     Number of times the clip has been viewed.
    """

    def __init__(self, user_id, self_init=True, **kwargs):
        if self_init:
            self.clip_data = call_api("clips?broadcaster_id={0}".format(user_id))['data'][0]

            self.user_id = user_id
            self.user_name = self.clip_data['broadcaster_name']
            self.created_at = self.clip_data['created_at']
            self.creator_id = self.clip_data['creator_id']
            self.creator_name = self.clip_data['creator_name']
            self.embed_url = self.clip_data['embed_url']
            self.game_id = self.clip_data['game_id']
            self.id = self.clip_data['id']
            self.language = self.clip_data['language']
            self.thumbnail_url = self.clip_data['thumbnail_url']
            self.title = self.clip_data['title']
            self.url = self.clip_data['url']
            self.video_id = self.clip_data['video_id']
            self.view_count = self.clip_data['view_count']

        if not self_init:
            self.user_id = user_id
            self.user_name = kwargs['broadcaster_name']
            self.created_at = kwargs['created_at']
            self.creator_id = kwargs['creator_id']
            self.creator_name = kwargs['creator_name']
            self.embed_url = kwargs['embed_url']
            self.game_id = kwargs['game_id']
            self.id = kwargs['id']
            self.language = kwargs['language']
            self.thumbnail_url = kwargs['thumbnail_url']
            self.title = kwargs['title']
            self.url = kwargs['url']
            self.video_id = kwargs['video_id']
            self.view_count = kwargs['view_count']


# Aliases
get_games = get_game
