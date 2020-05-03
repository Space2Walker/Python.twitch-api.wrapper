#      Copyright (C) 2020  Space2Walker
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import threading
import time
import twitch
from abos import abos
from subprocess import Popen

import gi

gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Notify


# todo lets see what happens works at the moment

def main_loop():
	first_round = True
	last_index = {}

	while True:
		# get data
		index = twitch.search('STREAMS', dicta=True, user_login=abos)

		if first_round:
			for user_id, stream in index.items():
				t1 = threading.Thread(target=show_notification,
									  args=[stream.name, stream.title,
											stream.url])
				t1.start()

		if not first_round:
			for user_id, stream in index.items():

				try:
					# Try to load last round user info
					last = last_index[user_id]
				except KeyError:
					# if load fails for last round the object must be new
					t2 = threading.Thread(target=show_notification,
										  args=[stream.name, stream.title,
												stream.url])
					t2.start()
				else:
					# compare last round and new data
					if (last.title != stream.title) or (
						last.game_id != stream.game_id):
						t3 = threading.Thread(target=show_notification,
											  args=[stream.name, stream.title,
													stream.url])
						t3.start()

		# copy last data and set 2nd round flag then wait
		last_index = index
		first_round = False
		time.sleep(300)


def callback(h, action='closed', url='None'):
	print(action, url, h)
	if action == 'dismiss':
		Gtk.main_quit()

	if action == 'play':
		command = ['streamlink', url, 'best', '-Q', '-p', 'cvlc']
		Popen(command)
		Gtk.main_quit()

	if action == 'closed':
		Gtk.main_quit()


def show_notification(name, title, url):
	Notify.init("Twitch")
	notification = Notify.Notification.new(name, title,
										   "/home/lord/Documents/Twitch/twitch.png")
	notification.add_action(
		"play",
		"Play",
		callback,
		url
	)
	notification.add_action(
		"dismiss",
		"Dismiss",
		callback,
		url
	)
	notification.connect('closed', callback)
	notification.timeout = 10000
	notification.show()
	Gtk.main()


if __name__ == '__main__':
	main_loop()
