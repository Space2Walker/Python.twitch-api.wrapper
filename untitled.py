
import helix

# streamer = helix.call_api("games?name=NHL+17&name=Redout")
game = helix.Vod('511802295')
# print(streamer)
print(game.title, game.type)

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
