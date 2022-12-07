from Scweet import user as twi_user
from Scweet import scweet
import urllib3
import tweepy

users = ['@EN__Ien', '@WaiFu8964']
proxy = "127.0.0.1:8964"
env = 'run.env'


print(env)

#users_info = twi_user.get_user_information(users, headless=False, proxy=proxy)
following = twi_user.get_users_following(users=users, verbose=0, headless=False, env=env, wait=2, file_path=None, proxy=proxy)
#followers = twi_user.get_users_followers(users=users, verbose=0, headless=False, env=env, wait=2, file_path=None, proxy=proxy)

print(following)



'''
user_id = 'EN__Ien'

auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAIqUkAEAAAAAgReIJ0H4I6dzHF7odxS4aJKaUaw%3DkeINxzbh21yrc8gTEGFduloCGYbe2yM1AbN2oXsXzxSXUFI2nJ")
api = tweepy.API(auth, proxy=proxy)
get_friendship = api.get_friends(user_id=user_id, cursor=-1)
print(get_friendship)
'''