#!/usr/bin/env python3
# author: Space2Walker
# 2019-11-28
"""The Twitch Module

Functions:

- call_api()
- search()
- get_hls()
- get_game()
- get_top_games()

Classes:

- Streamer()
- Stream()
- Vod()
- Clip()


"""
import requests
import streamlink

from helper import kwargs_to_query

api = "https://api.twitch.tv/helix/"
headers = {'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}


def call_api(uri):
    """
    Call`s the Api https://api.twitch.tv/helix/$uri

    :param uri: str
    :return: json object
    """
    # todo better error handling, rate limiting and removing requests

    response = requests.get(api + uri, headers=headers).json()
    try:
        if response['data']:
            return response

    except KeyError:
        raise Exception("NO DATA Your request didn't get any data back")


def search(identifier, **kwargs):
    """
    Full Doc Compatible See
    https://dev.twitch.tv/docs/api/reference/#get-streams
    https://dev.twitch.tv/docs/api/reference/#get-videos
    https://dev.twitch.tv/docs/api/reference/#get-clips

    :param identifier: 'STREAMS' OR 'VIDEOS' OR 'CLIP'
    :type identifier: str
    :param kwargs: user_login=['gronkh', 'lastmiles'], user_id=[49112900]
    :type kwargs: str or int or list
    :return: Stream Class Object or list of Objects
    :rtype: collections.defaultlist or Stream
    """
    ret = []

    # stick to your naming convention twitch for god sake
    if identifier.upper() == 'CLIPS':
        # renames the dict Key
        kwargs['broadcaster_id'] = kwargs.pop('user_id')

    req = kwargs_to_query(kwargs)
    res = call_api(f"{identifier.lower()}?{req}")['data']

    # convert api return to class
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
            ret.append(Clip(e['id'], self_init=False, **e))
        return ret


def get_hls(url, res='best'):
    """
    Crawls the HLS Url
    :param url: The Twitch video or Stream Url
    :type url: str
    :param res: 720p, 1080p and so on
    :type res: str
    :return: The HLS URL
    :rtype; str
    """
    # todo split into two functions and try do remove streamlink dependency
    streams = streamlink.streams(url)
    return streams[res].url


def get_game(**kwargs):
    """
    Gets game info`s
    https://dev.twitch.v/docs/api/reference#get-games

    :param kwargs: id= and/or name= 100 combined max
    :return: Json Containing the game data
    :rtype: list
    """
    request = kwargs_to_query(kwargs)

    return call_api(f"games?{request}")['data']


def get_top_games(first=100):
    """ Get the most Played Games/Categories
    https://dev.twitch.tv/docs/api/reference#get-top-games

    :param first: The amount of objects per Call
    :type first: int
    :return: Json Containing Game Info`s
    :rtype: list
    """
    return call_api(f"games/top?first={str(first)}")['data']


class Streamer:
    def __init__(self, name):
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
        - .follower: The Total amount of Followers the Channel has
        - .extensions: The Used Extensions

        :param name: The Url-save Streamer Name
        """
        # get basic info's for User
        user_data = call_api(f"users?login={name}")['data'][0]
        self.user_id = int(user_data['id'])
        self.name = name
        self.url = 'twitch.tv/' + name
        self.description = user_data['description']
        self.partner = user_data['broadcaster_type']
        self.profile_image_url = user_data['profile_image_url']
        self.offline_image_url = user_data['offline_image_url']
        self.total_views = int(user_data['view_count'])

    @property
    def extensions(self):
        """Get the Active Extensions used by Streamer

        :returns: Streamers Active Extensions
        :rtype: list or dict
        """
        extensions = call_api(f"users/extensions?user_id={self.user_id}")['data']
        e_index = []
        for e in extensions:
            for r in extensions[e]:
                if extensions[e][r]['active']:
                    del extensions[e][r]['active']
                    e_index.append({e: extensions[e][r]})
        return e_index[0]

    @property
    def follower(self):
        """Get Total Follower

        :returns: Total Follower
        :rtype: int
        """
        t_follow = call_api(
            f"users/follows?from_id={self.user_id}")['total']
        return int(t_follow)

    def follows(self, direction, first=100):
        """Yields the Users the Input is Following

        OR is Followed by

        :param direction: Follow Direction "TO" Streamer "FROM" Streamer
        :type direction: str
        :param first: Amount of Followers to Quarry if None gets All
        :type first: None or int
        :returns: Follower Info`s
        :rtype: Iterable[dict]
        """
        follows = None
        _follows_page = ''
        _follower_page = ''

        if (direction.upper() != 'TO') and (direction.upper() != 'FROM'):
            raise ValueError('Direction must be "TO" or "FROM"')

        while (first is None) or (first > 0):
            if direction.upper() == 'TO':
                follows = call_api(
                    f"users/follows?from_id={self.user_id}&first=100&after={_follows_page}")
                try:
                    _follows_page = follows['pagination']['cursor']
                except (KeyError, TypeError):
                    return

            if direction.upper() == 'FROM':
                follows = call_api(
                    f"users/follows?to_id={self.user_id}&first=100&after={_follower_page}")
                try:
                    _follower_page = follows['pagination']['cursor']
                except (KeyError, TypeError):
                    return

            del follows['pagination']
            for e in follows['data']:
                if first:
                    first = first - 1
                yield e

    # todo badges and emotes


class Stream(Streamer):
    def __init__(self, streamer, self_init=True, **kwargs):
        """A Class that representing the base Stats of a Stream"""
        if self_init:
            super(Stream, self).__init__(streamer)
            # get basic info`s of Stream
            self.stream_data = call_api(f"streams?user_id={self.user_id}")

            try:
                self.stream_id = self.stream_data['data'][0]['id']
                self.game_id = self.stream_data['data'][0]['game_id']
                self.type = self.stream_data['data'][0]['type']
                self.title = self.stream_data['data'][0]['title']
                self.viewers = self.stream_data['data'][0]['viewer_count']
                self.started_at = self.stream_data['data'][0]['started_at']
                self.language = self.stream_data['data'][0]['language']
                self.thumbnail_url = self.stream_data['data'][0]['thumbnail_url']
                self.tag_ids = self.stream_data['data'][0]['tag_ids']

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
        return call_api(f"streams/tags?broadcaster_id={self.user_id}")

    # todo get_meta https://dev.twitch.tv/docs/api/reference#get-streams-metadata
    # uses its one rate limiting


class Vod:
    def __init__(self, vod_id, self_init=True, **kwargs):
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

        :param vod_id: The Vod ID "513455174"
        """
        if self_init:
            self.vod_data = call_api(f"videos?id={vod_id}")['data'][0]

            self.vod_id = int(self.vod_data['id'])
            self.user_id = int(self.vod_data['user_id'])
            self.name = self.vod_data['user_name']
            self.url = self.vod_data['url']
            self.title = self.vod_data['title']
            self.description = self.vod_data['description']
            self.created_at = self.vod_data['created_at']
            self.published_at = self.vod_data['published_at']
            self.thumbnail_url = self.vod_data['thumbnail_url']
            self.viewable = self.vod_data['viewable']
            self.view_count = int(self.vod_data['view_count'])
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
    def __init__(self, clip_id, self_init=True, **kwargs):
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
        if self_init:
            self.clip_data = call_api(f"clips?id={clip_id}")['data'][0]

            self.clip_id = clip_id
            self.user_id = int(self.clip_data['broadcaster_id'])
            self.name = self.clip_data['broadcaster_name']
            self.created_at = self.clip_data['created_at']
            self.creator_id = int(self.clip_data['creator_id'])
            self.creator_name = self.clip_data['creator_name']
            self.embed_url = self.clip_data['embed_url']
            self.game_id = int(self.clip_data['game_id'])
            self.language = self.clip_data['language']
            self.thumbnail_url = self.clip_data['thumbnail_url']
            self.title = self.clip_data['title']
            self.url = self.clip_data['url']
            self.video_id = int(self.clip_data['video_id'])
            self.view_count = int(self.clip_data['view_count'])

        if not self_init:
            self.clip_id = clip_id
            self.user_id = kwargs['broadcaster_id']
            self.user_name = kwargs['broadcaster_name']
            self.created_at = kwargs['created_at']
            self.creator_id = kwargs['creator_id']
            self.creator_name = kwargs['creator_name']
            self.embed_url = kwargs['embed_url']
            self.game_id = kwargs['game_id']
            self.language = kwargs['language']
            self.thumbnail_url = kwargs['thumbnail_url']
            self.title = kwargs['title']
            self.url = kwargs['url']
            self.video_id = kwargs['video_id']
            self.view_count = kwargs['view_count']


# Aliases
get_games = get_game
