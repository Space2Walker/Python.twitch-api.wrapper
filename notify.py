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
last_index = {}
first_round = True


# notify helper
def show_notification(name, title):
    _notification = Notify.Notification.new(name, title, "/home/lord/Documents/Twitch/twitch.png")
    _notification.show()
    return


# run forever
while True:

    # get data
    index = twitch.search('STREAMS', dicta=True, user_login=abos)

    if first_round:
        for user_id, stream in index.items():
            show_notification(stream.name, stream.title)

    # todo must check if we compare the same streamer maybe by id
    # iterate over data an compare to last data
    if not first_round:
        for user_id, stream in index.items():
            last = None

            # there is now last wit that id so it must be new
            try:
                last = last_index[user_id]
            except KeyError:
                show_notification(stream.name, stream.title)

            if (last.title != stream.title) or (last.game_id != stream.game_id):
                show_notification(stream.name, stream.title)

    # copy last data and set 2nd run flag then wait
    last_index = index
    first_round = False
    time.sleep(300)
