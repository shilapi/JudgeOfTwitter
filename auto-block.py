import time

import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import urllib
from Scweet.const import get_username, get_password, get_email
import random
import json
import Scweet.utils as utils

def check_exists_by_xpath(xpath, driver):
    timeout = 3
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def init_driver(headless=True, proxy=None, show_images=False, option=None):
    """ initiate a chromedriver instance
        --option : other option to add (str)
    """

    # create instance of web driver
    chromedriver_path = chromedriver_autoinstaller.install()
    # options
    options = Options()
    if headless is True:
        print("Scraping on headless mode.")
        options.add_argument('--disable-gpu')
        options.headless = True
    else:
        options.headless = False
    options.add_argument('log-level=3')
    if proxy is not None:
        options.add_argument('--proxy-server=%s' % proxy)
        print("using proxy : ", proxy)
    if show_images == False:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
    if option is not None:
        options.add_argument(option)
    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    driver.set_page_load_timeout(100)
    return driver

def log_in(driver, env, timeout=20, wait=4):
    email = get_email(env)  # const.EMAIL
    password = get_password(env)  # const.PASSWORD
    username = get_username(env)  # const.USERNAME

    driver.get('https://twitter.com/i/flow/login')

    email_xpath = '//input[@autocomplete="username"]'
    password_xpath = '//input[@autocomplete="current-password"]'
    username_xpath = '//input[@data-testid="ocfEnterTextTextInput"]'

    sleep(random.uniform(wait, wait + 1))
    sleep(2)#for lag
    #print(email, password, username)

    # enter email
    email_el = driver.find_element_by_xpath(email_xpath)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(email)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))
    # in case twitter spotted unusual login activity : enter your username
    if check_exists_by_xpath(username_xpath, driver):
        username_el = driver.find_element_by_xpath(username_xpath)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(username)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(Keys.RETURN)
        sleep(random.uniform(wait, wait + 1))
    # enter password
    password_el = driver.find_element_by_xpath(password_xpath)
    password_el.send_keys(password)
    sleep(random.uniform(wait, wait + 1))
    password_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))

    def log_user_page(user, driver, headless=True, proxy=None):
        sleep(random.uniform(1, 2))
        driver.get('https://twitter.com/' + user)
        sleep(random.uniform(1, 2))

def log_user_page(user, driver, headless=True, proxy=None):
    sleep(random.uniform(1, 2))
    driver.get('https://twitter.com/' + user)
    sleep(random.uniform(1, 2))


def main():
    env = 'main.env'
    proxy = '127.0.0.1:8964' #Change ur proxy here or None
    filePath = 'outputs/' + 'Your json'
    driver = utils.init_driver(headless=False, proxy=proxy)
    log_in(driver, env, wait=3)
    with open(filePath, "r") as readF:
        users = json.load(readF)
    for i in users['suspects'] + users["socialCircleOfUser"]:
        print(i)
        log_user_page(i, driver)
        time.sleep(1)
        if_blocked = False
        try:
            notification = driver.find_element(by=By.XPATH, value="//div[contains(@data-testid,'sheetDialog')]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[1]")
            if notification.is_enabled():
                notification.click()
        except:
            print()
        try:
            unblock = driver.find_element(by=By.XPATH, value="//div[contains(@data-testid,'unblock')]")
            if_blocked = unblock.is_enabled()
        except:
            element = driver.find_element(by=By.XPATH, value="//div[contains(@data-testid,'userActions')]/div")
            #print(element.is_enabled())
            element.click()
            time.sleep(0.5)
            block = driver.find_element(by=By.XPATH, value="//div[contains(@data-testid,'block')]/div[2]")
            #print(block.is_enabled())
            block.click()
            time.sleep(0.5)
            comfrim = driver.find_element(by=By.XPATH, value="//div[contains(@data-testid,'confirmationSheetConfirm')]")
            #print(comfrim.is_enabled())
            comfrim.click()


if __name__ == "__main__":
    main()