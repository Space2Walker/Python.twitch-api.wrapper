#!/usr/bin/env python3
# author: Space2Walker
# 2019-09-12
from subprocess import Popen
from colorama import Fore, init
import helix
from Twitch import abos

init(autoreset=True)

index= []
n=1

# get infos
for user in abos:
    index.append(helix.Stream(user))

# sorting
def sortkey(val): 
	return val.type

index.sort(key = sortkey, reverse = False)  

# display results
for user in index:

    if user.type != "offline":
        print(str(n) + ".")
        print(Fore.GREEN + user.name)
        print(user.title)
    else:
        print(Fore.RED + user.name)

    n+=1

# get choice
choice = int(input("Number ?")) - 1

# play stream
stream = index[choice].get_hls('720p')

command= ['vlc', stream, '--meta-title', index[choice].title]

Popen(command)


