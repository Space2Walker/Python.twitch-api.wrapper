import twitch

#####################################################
#                  get extensions                   #
#####################################################
"""
streamer = twitch.Streamer('montanablack88')
extensions = streamer.extensions
print(extensions)
"""

#####################################################
#                   Search                          #
#####################################################
"""
# Get 100 most viewed Streams
test = twitch.search('Streams', first=['100'])
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
#           Iterate over all Followers             #
#####################################################

follow_gen = twitch.Streamer('lastmiles').follows('FROM')
for e in follow_gen:
    print(e)


#####################################################
#                   get_game                        #
#####################################################
"""
game = twitch.get_game(name=["FIFA 20"], id=[27471])
print(game)
"""
