from Scweet import user as twi_user
from Scweet.scweet import scrape
import re
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def reply_count(fromU, to, since, until, proxy):
    replys = scrape(to_account=to, from_account=fromU, since=since, until=until, interval=100, headless=True, display_type="Latest", save_images=False, proxy=proxy, save_dir='outputs', resume=False)
    replys_num = len(replys)
    return replys_num

def get_interact_tweets(userTo):
    proxy = None #replace with your http proxy here(or None)
    dateToday = time.strftime("%Y-%m-%d", time.localtime())
    strftimeI = time.strptime(joinDate[i], "%Y-%m-%d")
    strftimeJ = time.strptime(joinDate[userTo], "%Y-%m-%d")
    if strftimeI >= strftimeJ:
        dateSince = joinDate[i]
    else:
        dateSince = joinDate[userTo]
    a2bCount = int(reply_count(fromU=i, to=userTo, since=dateSince, until=dateToday, proxy=proxy))
    b2aCount = int(reply_count(fromU=userTo, to=i, since=dateSince, until=dateToday, proxy=proxy))
    # start judgement
    if a2bCount == 0 and b2aCount == 0:
        print('')
        return {}
    elif b2aCount == 0 and a2bCount != 0:
        return {'victims': [userTo]}
    elif a2bCount == 0 and b2aCount >= 4:
        return {'suspects': [userTo]}
    else:
        posibility = a2bCount / b2aCount
        if posibility >= 2.2 and b2aCount < 8:
            return {'victims': [userTo]}
        elif posibility >= 1 and posibility < 1.8 and b2aCount >= 8:
            return {'socialCircleOfUser': [userTo]}
        elif posibility < 1 and posibility >= 0.4 and b2aCount >= 8:
            return {'socialCircleOfUser': [userTo]}
        elif posibility < 0.4 and b2aCount >= 8:
            return {'suspects': [userTo]}

def callback(m):
    userType, user = m.result()
    return userType, user


if __name__ == '__main__' :
    users = ['@WaiFu8964', '@EN__Ien', ]#replace with your target user here
    proxy = None#replace with your http proxy here(or None)
    env = 'run.env'
    dateToday = time.strftime("%Y-%m-%d", time.localtime())
    limit = 65535

    #print(env)

    #start finding friends
    friends = {}
    joinDate = {}
    #get user's information
    for i in users :
        filePath = 'outputs/' + i + 'users_basic_info.json'
        if os.path.exists(filePath):
            with open(filePath, "r") as readF:
                userBasicInfo = json.load(readF)
            following = userBasicInfo['following']
            followers = userBasicInfo['followers']
            print(followers)
            print(following)
        else:
            following = twi_user.get_users_following(users=i, verbose=0, headless=False, env=env, wait=1,
                                                     file_path=None, proxy=proxy, limit=limit)
            followers = twi_user.get_users_followers(users=i, verbose=0, headless=False, env=env, wait=1,
                                                     file_path=None, proxy=proxy, limit=limit)
            usersInfo = {"following": following, "followers": followers}
            with open(filePath, "w") as write_file:
                json.dump(usersInfo, write_file, sort_keys=True, indent=4, separators=(', ', ': '))
            print(filePath + str(usersInfo))

        info, ifExist = twi_user.get_user_information(users=i, driver=None, headless=True, proxy=proxy)
        # print(info)
        if i in ifExist:
            continue
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
        filePath = 'outputs/' + 'users_friends_info.json'
        if os.path.exists(filePath):
            with open(filePath, "r") as readF:
                friendsBasicInfo = json.load(readF)
            friendInfo = friendsBasicInfo
            friends[i] = list(friendInfo.keys())
            print(friendInfo)
        else:
            friendInfo, lockedFriends = twi_user.get_user_information(users=friendsFindFormatted, driver=None, headless=True, proxy=proxy)
            for j in lockedFriends:
                friends[i].remove(j)
                friendInfo.pop(j, None)
            with open(filePath, "w") as write_file:
                json.dump(friendInfo, write_file, sort_keys=True, indent=4, separators=(', ', ': '))
            print(filePath + str(friendInfo))
        print(friendInfo)
        print(friends[i])
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
        personsOnTrail = {'victims': victims, 'suspects': suspects, 'socialCircleOfUser': socialCircleOfUser}
        with ThreadPoolExecutor(max_workers=10) as pool:
            for data in pool.map(get_interact_tweets,friends[i]):
                print(data)
                if data != {}:
                    for q, j in personsOnTrail.items():
                        try:
                            z = data[q]
                            print(z)
                            personsOnTrail[q].extend([x for x in z])
                            print(personsOnTrail)
                        except:
                            print('have no data'+q)

        #save file to json

        filePath = 'outputs/' + 'from' + '_' +str(i) + '_' + 'persons_on_trail.json'
        with open(filePath, "w") as write_file:
            json.dump(personsOnTrail, write_file, sort_keys=True, indent=4, separators=(', ', ': '))
        print(filePath + str(personsOnTrail))


"""            for j,q in result:
                if j == 'vic':
                    victims.append(q)
                elif j == 'sus':
                    suspects.append(q)
                elif j == 'cir':
                    socialCircleOfUser.append(q)"""


