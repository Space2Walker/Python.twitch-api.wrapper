#!/usr/bin/env python3
# author: Space2Walker
# 2019-09-12

from subprocess import Popen

from colorama import Fore, init

import twitch

with open('abos.txt', 'r') as opened_file:
    abos = opened_file.read()

init(autoreset=True)
n = 1

index = twitch.search('STREAMS', user_login=abos)


# sorting
def sortkey(val):
    return val.type


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
