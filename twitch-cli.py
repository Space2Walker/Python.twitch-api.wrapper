#!/usr/bin/env python3
# author: Space2Walker
# 2019-09-12

from subprocess import Popen

from colorama import Fore, init

import helix
from abos import abos

init(autoreset=True)

n = 1

# get info's
# for user in abos:
#     index.append(helix.Stream(user))
index = helix.search('STREAMS', user_login=abos)


# sorting
def sortkey(val):
    return val.type


index.sort(key=sortkey, reverse=False)

# display results
for user in index:

    if user.type != "offline":
        print(str(n) + ".")
        print(Fore.GREEN + user.user_name)
        print(user.title)
    else:
        print(Fore.RED + user.user_name)

    n += 1

# get choice
choice = int(input("Number ?")) - 1

# play stream
url = 'twitch.tv/' + str(index[choice].user_name)
stream = helix.get_hls(url, '720p')

command = ['vlc', stream, '--meta-title', index[choice].title]

Popen(command)
