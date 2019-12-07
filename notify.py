#!/usr/bin/env python3
# author: Space2Walker
# 2019-09-12
import time

import gi

import twitch

gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')

from abos import abos
from subprocess import Popen
from gi.repository import Notify
from gi.repository import Gtk


# play with streamlink
def play_this(obj, action, url):
    if action == 'dismiss':
        Gtk.main_quit()

    if action == 'play':
        command = ['streamlink', url, 'best', '-Q']
        Popen(command)
        Gtk.main_quit()


# notify helper
def show_notification(name, title, url):
    Notify.init("Twitch")
    notification = Notify.Notification.new(name, title, "/home/lord/Documents/Twitch/twitch.png")
    notification.add_action(
        "play",
        "Play",
        play_this,
        url  # Arguments
    )
    notification.add_action(
        "dismiss",
        "Dismiss",
        play_this,
        url  # Arguments
    )
    notification.show()
    # todo find a solution to the event based notification callback
    Gtk.main()


# run forever
def main():
    last_index = {}
    first_round = True
    # val setting

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
                if (last.title != stream.title) or (last.game_id != stream.game_id):
                    show_notification(stream.name, stream.title, stream.url)

    # copy last data and set 2nd run flag then wait
    last_index = index
    first_round = False
    time.sleep(300)


# import sys
#
# from gi.repository import Notify
# from gi.repository import Gtk
#
# if not Notify.init('Notification Test'):
#     print("ERROR: Could not init Notify.")
#     sys.exit(1)
#
# notification = Notify.Notification.new(
#     "Notification Title",
#     "Message...")
#
# notification.set_urgency(Notify.Urgency.NORMAL)
# def actionCallback(notification, action, user_data = None):
#     print("Callback called:"+action)
#     Gtk.main_quit()
#
# notification.add_action("test-action", "Test Action", actionCallback)
#
# if not notification.show():
#     print("ERROR: Could not show notification.")
#     sys.exit(2)
#
# Gtk.main()

if __name__ == '__main__':
    main()
