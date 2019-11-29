import twitch

res = twitch.call_api("users?login=gronkh")
print(res)
#####################################################
#                   Search                          #
#####################################################
"""
# Get 100 most viewed Streams
test = helix.search('Streams', first=['100'])
for stream in test:
    print(stream.user_name, stream.title, stream.viewers)
"""
"""
# check if Streamers are online
test = twitch.search('Streams', user_login=['gronkh', 'lastmiles'], user_id=49112900)
for stream in test:
    print(stream.user_name, stream.title, stream.viewers)
"""
#####################################################
#           Iterate over  all Followers             #
#####################################################
"""
miles = helix.Streamer('lastmiles')
while True:
    followers = miles.follows('FROM')
    if followers is None:
        break
    for follower in followers:
        print(follower['from_name'])
"""
#####################################################
#                   get_game                        #
#####################################################
"""
game = helix.get_game(name=["FIFA 20"], id=[27471])
print(game)
"""
