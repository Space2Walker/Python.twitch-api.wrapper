
import helix

streamer = helix.Streamer("lastmiles")
x = 1
while x != 0:

    for e in streamer.follower():
        if not e:
            x = 0
            break
        followers = e['data']

        for f in followers:
            print(f['from_name'])
