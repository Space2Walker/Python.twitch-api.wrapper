#!/usr/bin/env python3
# author: Space2Walker
# 2019-09-12
import gi
import time
from Twitch import Streamer
from Twitch import abos

gi.require_version('Notify', '0.7')
from gi.repository import Notify
Notify.init("Twitch")

last_index= []
second_run= 0

while True:
	index = []
	for user in abos:
		index.append(Streamer(user))
		
	n=0
	for user in index:
		if second_run:
			if user.status and (last_index[n].title != user.title or last_index[n].game_id != user.game_id):
				Hello = Notify.Notification.new(user.name, user.title, "/home/lord/Documents/Twitch/twitch.png")
				Hello.show()
		else:		
			if user.status:
				Hello = Notify.Notification.new(user.name, user.title, "/home/lord/Documents/Twitch/twitch.png")
				Hello.show()
		n+=1

	last_index = index
	second_run = 1
	time.sleep(300)