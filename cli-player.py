#!/usr/bin/env python3
# author: Space2Walker
# 2019-09-12


import argparse
from subprocess import Popen

from colorama import Fore, init

import twitch
from abos import abos

site = "https://twitch.tv/"


# sorting
def sortkey(val):
    return val.type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--play', help='Plays the Stream of a given user', type=str)

    args = parser.parse_args()
    if args.play:
        url = site + args.play
        command = ['streamlink', url, 'best']
        Popen(command)

    else:
        choice()


def choice():
    init(autoreset=True)
    n = 1
    index = twitch.search('STREAMS', user_login=abos)

    index.sort(key=sortkey, reverse=False)

    # display results
    for user in index:

        if user.type != "offline":
            print(str(n) + ".")
            print(Fore.GREEN + user.name)
            print(user.title)

        n += 1

    # get choice
    choice = int(input("Number ?")) - 1

    # play stream
    url = 'twitch.tv/' + str(index[choice].name)
    stream = twitch.get_hls(url, 'best')

    command = ['vlc', stream, '--meta-title', index[choice].title]

    Popen(command)


if __name__ == '__main__':
    main()
