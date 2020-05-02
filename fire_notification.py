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

import argparse
from subprocess import Popen

import gi

gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Notify


# play with streamlink
def play_this(h, action='closed', url='None'):
	print(action, url, h)
	if action == 'dismiss':
		Gtk.main_quit()
		exit(0)

	if action == 'play':
		command = ['streamlink', url, 'best', '-Q', '-p', 'cvlc']
		Popen(command)
		Gtk.main_quit()
		exit(0)

	if action == 'closed':
		Gtk.main_quit()
		exit(0)

	exit(0)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--name', type=str)
	parser.add_argument('-t', '--title', type=str)
	parser.add_argument('-u', '--url', type=str)
	args = parser.parse_args()
	Notify.init("Twitch")
	notification = Notify.Notification.new(args.name, args.title,
										   "/home/lord/Documents/Twitch/twitch.png")
	notification.add_action(
		"play",
		"Play",
		play_this,
		args.url
	)
	notification.add_action(
		"dismiss",
		"Dismiss",
		play_this,
		args.url
	)
	notification.connect('closed', play_this)
	# notification.timeout = 10000
	notification.show()

	# todo find a solution to the event based notification callback
	Gtk.main()


if __name__ == '__main__':
	main()
	exit(0)
