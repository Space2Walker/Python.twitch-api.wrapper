#!/usr/bin/env python3
# author: Space2Walker
# 2019-09-12
import subprocess
import time
from os import path as opath
from sys import path as spath

import twitch
from abos import abos


# notify helper
def show_notification(name, title, url):
	file = opath.join(spath[0], "fire_notification.py")
	command = ['python', file, '-n', name, '-t', title, '-u', url]
	subprocess.DETACHED_PROCESS = 1
	subprocess.Popen(command)


# run forever
def main():
	last_index = {}
	first_round = True

	# get data
	index = twitch.search('STREAMS', dicta=True, user_login=abos)

	if first_round:
		for user_id, stream in index.items():
			show_notification(stream.name, stream.title, stream.url)

	# iterate over data an compare to last data
	if not first_round:
		for user_id, stream in index.items():
			last = None
			# there is now last wit that id so it must be new
			try:
				last = last_index[user_id]
			except KeyError:
				show_notification(stream.name, stream.title, stream.url)
			else:
				if (last.title != stream.title) or (
					last.game_id != stream.game_id):
					show_notification(stream.name, stream.title, stream.url)

	# copy last data and set 2nd run flag then wait
	last_index = index
	first_round = False
	time.sleep(300)


if __name__ == '__main__':
	main()
