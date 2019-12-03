#!/usr/bin/env python3
# author: Space2Walker
# 2019-09-12

import argparse
from subprocess import Popen

from colorama import Fore, init

import twitch
from abos import abos

site = "https://twitch.tv/"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--play', help='Plays the Stream of a given user', type=str)
    parser.add_argument('-v', '--vod', help='Shows the latest VOD`s of a given user', type=str)
    args = parser.parse_args()

    if args.play:
        url = site + args.play
        play(url)

    if args.vod:
        vod(args.vod)

    else:
        display()


# sorting
def sortkey(val):
    return val.type


# play with streamlink
def play(url):
    command = ['streamlink', url, 'best', '-Q']
    Popen(command)


# get choice
def choice():
    user_input = None

    try:
        user_input = int(input("Number ?")) - 1
    except KeyboardInterrupt:
        exit()

    return user_input


def vod(user_name):
    init(autoreset=True)
    n = 1
    user_id = twitch.Streamer(user_name).user_id
    index = twitch.search('VIDEOS', user_id=user_id, first=10)

    for vid in index:
        print(str(n) + ".")
        print(Fore.GREEN + vid.title)
        print(vid.duration)
        n += 1

    # get choice
    user_input = choice()

    url = str(index[user_input].url)
    play(url)


# display online Streams from Abo`s
def display():
    init(autoreset=True)
    n = 1

    index = twitch.search('STREAMS', user_login=abos)

    index.sort(key=sortkey, reverse=False)

    # display results
    for user in index:
        print(str(n) + ".")
        print(Fore.GREEN + user.name)
        print(user.title)
        n += 1

    # get choice
    user_input = choice()

    url = site + str(index[user_input].name)
    play(url)


if __name__ == '__main__':
    main()
