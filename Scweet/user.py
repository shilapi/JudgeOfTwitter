import time
import os
import Scweet.utils as utils
from time import sleep
import random
import json


def get_user_information(users, driver=None, headless=True, proxy=None):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless, proxy=proxy)

    users_info = {}
    empty_users = []

    for i, user in enumerate(users):

        log_user_page(user, driver)
        time.sleep(3)

        if user is not None:

            try:
                following = driver.find_element_by_xpath('//a[contains(@href,"/following")]/span[1]/span[1]').text
                followers = driver.find_element_by_xpath('//a[contains(@href,"/followers")]/span[1]/span[1]').text
            except Exception as e:
                following = ''
                followers = ''
                print('...')
            try:
                element = driver.find_element_by_xpath('//div[contains(@data-testid,"UserProfileHeader_Items")]//a[1]')
                website = element.get_attribute("href")
            except Exception as e:
                # print(e)
                website = ""

            try:
                desc = driver.find_element_by_xpath('//div[contains(@data-testid,"UserDescription")]').text
            except Exception as e:
                # print(e)
                desc = ""
            a = 0
            try:
                join_date = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[4]').text
                birthday = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[3]').text
                location = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
            except Exception as e:
                try:
                    join_date = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[3]').text
                    birthday = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                    location = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                except Exception as e:
                    # print(e)
                    try:
                        join_date = driver.find_element_by_xpath(
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                        span1 = driver.find_element_by_xpath(
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                        if hasNumbers(span1):
                            birthday = span1
                            location = ""
                        else:
                            location = span1
                            birthday = ""
                    except Exception as e:
                        # print(e)
                        try:
                            join_date = driver.find_element_by_xpath(
                                '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                            birthday = ""
                            location = ""
                        except Exception as e:
                            # print(e)
                            join_date = ""
                            birthday = ""
                            location = ""
                            empty_users.append(user)
            print("--------------- " + user + " information : ---------------")
            print("Following : ", following)
            print("Followers : ", followers)
            print("Location : ", location)
            print("Join date : ", join_date)
            print("Birth date : ", birthday)
            print("Description : ", desc)
            print("Website : ", website)
            users_info[user] = [following, followers, join_date, birthday, location, website, desc]

            if i == len(users) - 1:
                driver.close()
                return users_info, empty_users
        else:
            print("You must specify the user")
            continue


def log_user_page(user, driver, headless=True, proxy=None):
    sleep(random.uniform(1, 2))
    driver.get('https://twitter.com/' + user)
    sleep(random.uniform(1, 2))


def get_users_followers(users, env=None, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None, proxy=None):
    followers = utils.get_users_follow(users, headless, env, "followers", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    with open(file_path, 'w') as f:
        json.dump(followers, f)
        print(f"file saved in {file_path}")
    return followers


def get_users_following(users, env=None, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None, proxy=None):
    following = utils.get_users_follow(users, headless, env, "following", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open(file_path, 'w') as f:
        json.dump(following, f)
        print(f"file saved in {file_path}")
    return following


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
