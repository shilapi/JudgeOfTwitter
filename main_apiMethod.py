import urllib3
import tweepy

user_id = 'EN__Ien'

auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAIqUkAEAAAAAgReIJ0H4I6dzHF7odxS4aJKaUaw%3DkeINxzbh21yrc8gTEGFduloCGYbe2yM1AbN2oXsXzxSXUFI2nJ")
api = tweepy.API(auth, proxy=proxy)
get_friendship = api.get_friends(user_id=user_id, cursor=-1)
print(get_friendship)