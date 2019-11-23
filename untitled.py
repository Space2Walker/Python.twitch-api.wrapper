
import helix

streamer = helix.Streamer("lastmiles")
print(list(streamer.follows('TO')))

# x = 1
# while x != 0:
#
#     for e in streamer.follows():
#         if not e:
#             x = 0
#             break
#         followers = e['data']
#
#         for f in followers:
#             print(f['from_name'])
