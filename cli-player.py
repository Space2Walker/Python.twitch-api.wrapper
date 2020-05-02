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

from colorama import Fore, init

import twitch
from abos import abos

site = "https://twitch.tv/"


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--play', help='Plays the Stream of a given user',
						type=str)
	parser.add_argument('-v', '--vod',
						help='Shows the latest VOD`s of a given user', type=str)
	args = parser.parse_args()

	if args.play:
		url = site + args.play
		play(url)

	if args.vod:
		vod(args.vod)

	else:
		stream()


# display options and get choice
def display(index, typ='stream'):
	init(autoreset=True)
	user_input = None

	for n, val in enumerate(index, start=1):
		print(str(n) + ".")
		if typ == 'stream':
			print(Fore.GREEN + val.name)
			print(val.title)
		if typ == 'vod':
			print(Fore.GREEN + val.title)
			print(val.duration)

	try:
		user_input = int(input("Number ?")) - 1
	except KeyboardInterrupt:
		print('\n')
		exit()

	return user_input


def play(url):
	# play with streamlink
	command = ['streamlink', url, 'best', '-Q', '-p', 'cvlc']
	Popen(command)


def vod(user_name):
	# get data
	user_id = twitch.Streamer(user_name).user_id
	index = twitch.search('VIDEOS', user_id=user_id, first=10)

	# display options and get choice
	user_input = display(index, typ='vod')

	# play
	url = str(index[user_input].url)
	play(url)


def stream():
	# get data
	index = twitch.search('STREAMS', user_login=abos)

	# display options and get choice
	user_input = display(index)

	# play
	url = site + str(index[user_input].name)
	play(url)


if __name__ == '__main__':
	main()
