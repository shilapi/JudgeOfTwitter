import urllib3
import tweepy

user_id = '@elonmusk' #replace with your target user

auth = tweepy.OAuth2BearerHandler(YourOAuthKey)
api = tweepy.API(auth, proxy=proxy)
get_friendship = api.get_friends(user_id=user_id, cursor=-1)
print(get_friendship)
