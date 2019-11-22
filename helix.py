#!/usr/bin/env python3
# author: Space2Walker
# 2019-10-18

import requests
import streamlink
from urllib.parse import urlencode


class Twitch:
	"""Twitch Class"""
	def __init__(self):
		self.api = "https://api.twitch.tv/helix/"
		self.headers = {'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}

	def call_api(self, uri):
		response = requests.get(self.api + uri, headers=self.headers)
		#print(response.headers)
		return response

	#def search(self, after=None ,before=None, first=20, game_id=None, language=None, user_id=None, user_login=None):
	def search(**kwargs):
		'''Full Doc Compatible See https://dev.twitch.tv/docs/api/reference/#get-streams'''
		req = urlencode(kwargs)
		res = Twitch().call_api("streams?{0}".format(req)).json()
		return res

	def get_game(self, game_id):
		game_data = Twitch().call_api("games?id={0}".format(game_id))
		return game_data



class Streamer(Twitch):
	"""docstring for ClassName"""
	def __init__(self, name):
		super(Streamer, self).__init__()
		self.name = name
		self.url = 'twitch.tv/' + name

		#get basic infos for User
		user_data = Twitch().call_api("users?login={0}".format(self.name)).json()
		self.user_data = user_data
		
		self.user_id = user_data['data'][0]['id']
		self.description = user_data['data'][0]['description']
		self.partner = user_data['data'][0]['broadcaster_type'] 
		self.profile_image_url = user_data['data'][0]['profile_image_url']
		self.offline_image_url = user_data['data'][0]['offline_image_url']
		self.total_views = user_data['data'][0]['view_count']
		 
	
	def follows(self, first=100, page=''):
		"""Get the Users the Input is Following (Pagination)"""
		follows = Twitch().call_api("users/follows?from_id={0}&first={1}&after={2}".format(self.user_id, first, page)).json()
		return follows

	def follower(self, first=20, page=''):
		"""Get the Users that Following the Input(Pagination)"""
		follower = Twitch().call_api("users/follows?to_id={0}&first={1}&after={2}".format(self.user_id, first, page)).json()
		return follower

	def extensions(self):
		"""Get the Extensions used in Stream"""
		extensions = Twitch().call_api("users/extensions?user_id={0}".format(self.user_id)).json()
		return extensions

	def clips(self):
		"""Get Clips"""
		self.clips = Twitch().call_api("clips?broadcaster_id={0}".format(self.user_id)).json()
		return self.clips

	def vod(self):
		"""Get VOD"""
		self.vod = Twitch().call_api("videos?user_id={0}".format(self.user_id)).json()
		return self.vod
	

class Stream(Streamer):
	"""docstring for Stream"""
	def __init__(self, streamer):
		super(Stream, self).__init__(streamer)
		#get basic infos for Streams
		stream_data = Twitch().call_api("streams?user_id={0}".format(self.user_id)).json()
		self.stream_data = stream_data

		if stream_data['data']:
			self.stream_id = stream_data['data'][0]['id']
			self.game_id = stream_data['data'][0]['game_id']
			self.type = stream_data['data'][0]['type']
			self.title = stream_data['data'][0]['title']
			self.viewers = stream_data['data'][0]['viewer_count']
			self.started_at = stream_data['data'][0]['started_at']
			self.language = stream_data['data'][0]['language']
			self.thumbnail_url = stream_data['data'][0]['thumbnail_url']
			self.tag_ids = stream_data['data'][0]['tag_ids']
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
		self.streams = streamlink.streams(self.url)
		self.stream = self.streams[res].url
		return self.stream

	def get_tags(self):
		"""Get the Tags of the Stream"""
		self.tags = Twitch().call_api("streams/tags?broadcaster_id={0}".format(self.user_id)).json()
		return self.tags['data']
	


# static-cdn.jtvnw.net/emoticons/v1/115390/1.0

k_api = "https://api.twitch.tv/kraken/"
k_headers = {'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}

def call_kraken(**kwargs):
	response = requests.get(api + kwargs, headers=headers)
		#print(response.headers)
	return response


# e_set = call_api('chat/emoticon_images?emotesets=19151')

