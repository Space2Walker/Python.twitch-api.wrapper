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
        exit()

    return user_input


# play with streamlink
def play(url):
    command = ['streamlink', url, 'best', '-Q']
    Popen(command)


######################################
#           Main Functions           #
######################################
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
    user_input = display(index, typ='stream')

    # play
    url = site + str(index[user_input].name)
    play(url)


if __name__ == '__main__':
    main()
