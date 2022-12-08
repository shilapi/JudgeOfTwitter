from Scweet import user as twi_user
from Scweet import scweet
from Scweet.scweet import scrape
import pandas as pd

def interact_frequency():
    return

def reply_count(fromU, to, since, until, proxy):
    replys = scrape(to_account=to, from_account=fromU, since=since, until=until, interval=10, headless=False, display_type="Latest", save_images=False, proxy=proxy, save_dir='outputs', resume=False)
    replys_num = len(replys)
    return replys_num

if __name__ == '__main__' :
    users = ['@EN__Ien']
    proxy = "127.0.0.1:8964"
    env = 'run.env'

    print(env)

    #users_info = twi_user.get_user_information(users, headless=False, proxy=proxy)
    following = twi_user.get_users_following(users=users, verbose=0, headless=False, env=env, wait=1, file_path=None, proxy=proxy, limit=50)
    followers = twi_user.get_users_followers(users=users, verbose=0, headless=False, env=env, wait=1, file_path=None, proxy=proxy, limit=50)
    info = twi_user.get_user_information(users=users, driver=None, headless=False, proxy=proxy)
    #print(following)

    #start finding friends
    friends = {}
    joinDate = {}
    for i in users :
        currentUserFollowing = following[i]
        currentUserFollowers = followers[i]
        currentUserInfo = info[i]
        currentUserJoinDate = currentUserInfo[3]
        friendsFind = [x for x in currentUserFollowing if x in currentUserFollowers]
        print(friendsFind)
        friends[i] = friendsFind
        joinDate[i] = currentUserJoinDate

    for i in users:
        for q in friends[i]:
            aTObCount = reply_count(fromU=i, to=q, since='2022-11-11', until='2022-12-9', proxy=proxy)






