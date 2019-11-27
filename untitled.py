
import helix

# streamer = helix.call_api("games?name=NHL+17&name=Redout")
# game = helix.Streamer('r4yman')
# print(game.follows('TO'))
#
# print(game.follows('TO'))

test = helix.search('VIDEOS', user_login=['lastmiles'], user_id=[49112900])
print(test[0])

# kwar = {'test': 123, 'use': 543}
# for e in kwar.keys():
#     print(e)

# for e in game:
#     print(e.user_name + "\n" + e.title)
# print(streamer)


# test = helix.Stream('lastmiles')
# print(test.title)
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
