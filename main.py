from Scweet import user as twi_user
from Scweet import scweet

users = ['@EN__Ien', '@WaiFu8964']
proxy = "127.0.0.1:8964"
env = 'run.env'

print(env)

#users_info = twi_user.get_user_information(users, headless=False, proxy=proxy)
following = twi_user.get_users_following(users=users, verbose=0, headless=False, env=env, wait=2, limit=50, file_path=None, proxy=proxy)
followers = twi_user.get_users_followers(users=users, verbose=0, headless=False, env=env, wait=2, limit=50, file_path=None, proxy=proxy)

print(users_info, followers, following)
