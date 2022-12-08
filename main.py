from Scweet import user as twi_user
from Scweet import scweet
from Scweet.scweet import scrape
import pandas as pd
import re
import time
import json
import tweepy

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
    dateToday = time.strftime("%Y-%m-%d", time.localtime())
    limit = 20

    #print(env)

    following = twi_user.get_users_following(users=users, verbose=0, headless=False, env=env, wait=1, file_path=None, proxy=proxy, limit=limit)
    followers = twi_user.get_users_followers(users=users, verbose=0, headless=False, env=env, wait=1, file_path=None, proxy=proxy, limit=limit)
    info, ifExist = twi_user.get_user_information(users=users, driver=None, headless=False, proxy=proxy)
    #print(info)
    for j in ifExist:
        users.remove(j)

    #start finding friends
    friends = {}
    joinDate = {}
    #get user's information
    for i in users :
        currentUserFollowing = following[i]
        currentUserFollowers = followers[i]
        currentUserInfo = info[i]
        print(currentUserInfo)
        currentUserJoinDate = currentUserInfo[2]
        joinDateFormatted = '%s-%s-1'%(re.findall(r"\d+", currentUserJoinDate)[0], re.findall(r"\d+", currentUserJoinDate)[1])
        print(joinDateFormatted)
        friendsFind = [x for x in currentUserFollowing if x in currentUserFollowers]
        friendsFindFormatted = []
        #格式化用户名 去掉@
        for j in friendsFind:
            friendsFindFormatted.append(j[1:])
        print(friendsFindFormatted)
        friends[i] = friendsFindFormatted
        joinDate[i] = joinDateFormatted
        # get friend's join date
        friendInfo, lockedFriends = twi_user.get_user_information(users=friendsFindFormatted, driver=None, headless=False, proxy=proxy)
        print(friendInfo)
        for j in lockedFriends:
            friends[i].remove(j)
        for j in friends[i]:
            currentUserInfo = friendInfo[j]
            currentUserJoinDate = currentUserInfo[2]
            joinDateFormatted = '%s-%s-1' % (re.findall(r"\d+", currentUserJoinDate)[0], re.findall(r"\d+", currentUserJoinDate)[1])
            print(joinDateFormatted)
            joinDate[j] = joinDateFormatted

        #get interact frequency
        victims = []
        suspects = []
        socialCircleOfUser = []
        for j in friends[i]:
            a2bCount = int(reply_count(fromU=i, to=j, since=joinDate[i], until=dateToday, proxy=proxy))
            b2aCount = int(reply_count(fromU=j, to=i, since=joinDate[j], until=dateToday, proxy=proxy))
            #start judgement
            posibility = a2bCount/b2aCount
            if b2aCount == 0 and a2bCount != 0:
                victims.append(j)
                break
            if a2bCount == 0 and b2aCount >= 4:
                suspects.append(j)
                break
            if posibility >= 2.2:
                victims.append(j)
                break
            if posibility >= 1 and posibility < 1.8:
                socialCircleOfUser.append(j)
                break
            if posibility <1 and posibility >= 0.4:
                socialCircleOfUser.append(j)
                break
            if posibility < 0.4:
                suspects.append(j)
                break

    #save file to json
    for i in users:
        filePath = 'outputs/' + 'from' + '_' +str(i) + '_' + 'persons_on_trail.json'
        personsOnTrail = {'victims': victims, 'suspects': suspects, 'socialCircleOfUser': socialCircleOfUser}
        with open(filePath, "w") as write_file:
            json.dump(personsOnTrail, write_file, sort_keys=True, indent=4, separators=(', ', ': '))
        print(filePath + str(personsOnTrail))






