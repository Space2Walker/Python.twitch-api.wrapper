#!/usr/bin/env python3
# author: Space2Walker
# 2019-09-12
import time

import gi

import twitch
from abos import abos

# Notify setup
gi.require_version('Notify', '0.7')
# noinspection PyUnresolvedReferences
from gi.repository import Notify
Notify.init("Twitch")

# val setting
last_index = []
first_round = True

# run forever
while True:

    # get data
    index = twitch.search('STREAMS', user_login=abos)

    if first_round:
        for user in index:
            notification = Notify.Notification.new(user.name, user.title, "/home/lord/Documents/Twitch/twitch.png")
            notification.show()

    # todo must check if we compare the same streamer maybe by id
    # iterate over data an compare to last data
    if not first_round:
        # zip new and old index together
        for new, last in zip(index, last_index):
            if (last.title != new.title) or (last.game_id != new.game_id):
                notification = Notify.Notification.new(new.name, new.title, "/home/lord/Documents/Twitch/twitch.png")
                notification.show()

    # copy last data and set 2nd run flag then wait
    last_index = index
    first_round = False
    time.sleep(300)
