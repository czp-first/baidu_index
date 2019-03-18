import json
import re

import pymongo
import time
import requests
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import urllib.parse

TIMEOUT = 5


def get_cookie():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, TIMEOUT)
    url = "https://www.baidu.com/"
    driver.get(url=url)
    driver.delete_all_cookies()
    button = wait.until(EC.element_to_be_clickable((By.XPATH, ("//div[@id='u1']/a[@name='tj_login']"))))
    button.click()
    sao = input("--请扫码--: ")
    cookie_list = driver.get_cookies()
    with open("cookie.txt", "w") as f:
        json.dump(cookie_list, f)
    driver.quit()


def test():
    driver = webdriver.Chrome()
    driver.delete_all_cookies()
    with open("cookie.txt", "r") as f:
        cookie_list = json.load(f)
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    driver.get("https://index.baidu.com")
    time.sleep(10)
    print(driver.get_cookies())
    driver.quit()


def login_one():
    """
    直接在百度指数，使用账号和密码登陆
    最后总有问题
    :return:
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, TIMEOUT)
    url = "https://index.baidu.com/"
    driver.get(url)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, ("//div[@class='links-item link-cursor links-item-unlogin']"))))
    button.click()
    input_username = wait.until(EC.element_to_be_clickable((By.XPATH, ("//input[contains(@class, 'pass-text-input pass-text-input-userName')]"))))
    input_username.click()
    input_username.send_keys("username")
    input_password = wait.until(EC.element_to_be_clickable((By.XPATH, ("//input[contains(@class, 'pass-text-input pass-text-input-password')]"))))
    input_password.click()
    input_password.send_keys("password!")

    submit = wait.until(EC.element_to_be_clickable((By.XPATH, ("//input[@class='pass-button pass-button-submit']"))))
    submit.click()

    time.sleep(2)
    if "验证码" in driver.page_source:
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, ("//input[contains(@class, 'forceverify-button forceverify-button-send') and contains(@id, 'mobile')]"))))
        send_button.click()
        verification = input("请输入验证码：")
        verification_input = wait.until(EC.element_to_be_clickable((By.XPATH, ("//input[contains(@class, 'forceverify-input forceverify-input-vcode')]"))))
        # verification_input.click()
        driver.execute_script("arguments[0].click();", verification_input)
        verification_input.send_keys(verification)
        time.sleep(1)
        verification_submit = wait.until(EC.element_to_be_clickable((By.XPATH, ("//input[contains(@class, 'forceverify-button forceverify-button-submit')]"))))
        verification_submit.click()
        if "系统错误，休息一会儿，请稍后再试" in driver.page_source:
            driver.quit()


def login():
    """

    :return: 带有登陆信息的会话
    """
    with open("cookie.txt", "r") as f:
        cookie_list = json.load(f)

    s = requests.session()
    s.verify = False
    s.headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "index.baidu.com",
        "Referer": "https://index.baidu.com/v2/main/index.html",
        "User-Agent": UserAgent().random
    }

    # 添加cookie
    jar = RequestsCookieJar()
    for cookie in cookie_list:
        jar.set(cookie["name"], cookie["value"])
    s.cookies = jar
    return s


def crawl_search(s, word):
    """
    获取搜索指数的数据
    :param s: 带有登陆信息的会话
    :return:
    """
    print("search")
    word = word.replace("（", "").replace("）", "").strip()
    # search_part_base_url = "https://index.baidu.com/api/SearchApi/index?"
    # ptbk_base_url = "https://index.baidu.com/Interface/ptbk?uniqid={}"
    # search_part_params = {
    #     "word": word,
    #     "area": 0,
    #     "days": 30
    # }
    # search_part_url = search_part_base_url + urllib.parse.urlencode(search_part_params)
    # search_part_response = s.get(search_part_url)
    # time.sleep(3)
    # search_part_response.encoding = "utf-8"
    # search_part_data_dict = json.loads(search_part_response.text)
    # uniqid用于获取映射表
    # if not search_part_data_dict.get("data"):
    #     return None
    # uniqid = search_part_data_dict.get("data").get("uniqid")
    #
    # ptbk_url = ptbk_base_url.format(uniqid)
    # ptbk_response = s.get(ptbk_url)
    # 映射表的原始数据
    # map_list = json.loads(ptbk_response.text).get("data")
    # print("映射表：")
    # print(map_list)

    # 搜索指数最近30天的数据，all=pc+wise，pc=pc端，wise=移动端
    # search_part_all = search_part_data_dict.get("data").get("userIndexes")[0].get("all").get("data")
    # search_part_pc = search_part_data_dict.get("data").get("userIndexes")[0].get("pc").get("data")
    # search_part_wise = search_part_data_dict.get("data").get("userIndexes")[0].get("wise").get("data")
    # print("最近30天数据：")
    # search_part_all_data = decrypt(map_list, search_part_all)
    # search_part_pc_data = decrypt(map_list, search_part_pc)
    # search_part_wise_data = decrypt(map_list, search_part_wise)
    # word = word

    # 搜索指数最近30天数据的概览
    # search_part_general_all = search_part_data_dict.get("data").get("generalRatio")[0].get("all")
    # search_part_general_pc = search_part_data_dict.get("data").get("generalRatio")[0].get("pc")
    # search_part_general_wise = search_part_data_dict.get("data").get("generalRatio")[0].get("wise")

    # print("最近30天数据概览：")
    # search_part_general_all_data = decrypt(map_list, search_part_general_all)
    # search_part_general_pc_data = decrypt(map_list, search_part_general_pc)
    # search_part_general_wise_data = decrypt(map_list, search_part_general_wise)
    # word = word
    # search_part_general_data_type = search_part_data_dict.get("data").get("generalRatio")[0].get("type")



    # 请求搜索指数所有数据接口
    search_all_base_url = "https://index.baidu.com/api/SearchApi/thumbnail?"
    search_all_params = {
        "area": 0,
        "word": word
    }
    search_all_url = search_all_base_url + urllib.parse.urlencode(search_all_params)
    search_all_response = s.get(url=search_all_url)
    search_all_data_dict = json.loads(search_all_response.text)

    if not search_all_data_dict.get("data"):
        return None

    ptbk_base_url = "https://index.baidu.com/Interface/ptbk?uniqid={}"
    uniqid = search_all_data_dict.get("data").get("uniqid")
    ptbk_url = ptbk_base_url.format(uniqid)
    ptbk_response = s.get(ptbk_url)
    time.sleep(3)
    # 映射表的原始数据
    map_list = json.loads(ptbk_response.text).get("data")

    # 获取搜索指数所有数据
    search_all_all = search_all_data_dict.get("data").get("all").get("data")
    search_all_pc = search_all_data_dict.get("data").get("pc").get("data")
    search_all_wise = search_all_data_dict.get("data").get("wise").get("data")

    # print("所有数据：")
    word = word
    search_all_all_data = decrypt(map_list, search_all_all)
    search_all_all_start_date = search_all_data_dict.get("data").get("all").get("startDate")
    search_all_all_end_date = search_all_data_dict.get("data").get("all").get("endDate")
    index_type = "search"
    data_type = "day"

    item = {
        "word": word,
        "index_type": index_type,
        "data": search_all_all_data,
        "start_date": search_all_all_start_date,
        "end_date": search_all_all_end_date,
        "data_type": data_type
    }
    print(item)
    return item

    # search_all_wise_data = decrypt(map_list, search_all_wise)
    # search_all_wise_start_date = search_all_data_dict.get("data").get("wise").get("startDate")
    # search_all_wise_end_date = search_all_data_dict.get("data").get("wise").get("endDate")
    # search_all_pc_data = decrypt(map_list, search_all_pc)
    # search_all_pc_start_date = search_all_data_dict.get("data").get("pc").get("startDate")
    # search_all_pc_end_date = search_all_data_dict.get("data").get("pc").get("endDate")


def crawl_news(s, word):
    print("news")
    word = word.replace("（", "").replace("）", "").strip()
    # 获取资讯指数的最近30天数据
    # news_part_base_url = "https://index.baidu.com/api/FeedSearchApi/getFeedIndex?"
    # news_part_params = {
    #     "word": word,
    #     "area": 0,
    #     "days": 30
    # }
    # news_part_url = news_part_base_url + urllib.parse.urlencode(news_part_params)
    # news_part_response = s.get(url=news_part_url)
    # time.sleep(3)
    # news_part_data_dict = json.loads(news_part_response.text)
    # if not news_part_data_dict.get("data"):
    #     return None
    #
    # ptbk_base_url = "https://index.baidu.com/Interface/ptbk?uniqid={}"
    # uniqid = news_part_data_dict.get("data").get("index")[0].get("uniqid")
    # ptbk_url = ptbk_base_url.format(uniqid)
    # ptbk_response = s.get(ptbk_url)
    # time.sleep(3)
    # 映射表的原始数据
    # map_list = json.loads(ptbk_response.text).get("data")

    # news_part = news_part_data_dict.get("data").get("index")[0].get("data")
    # news_part_general = news_part_data_dict.get("data").get("index")[0].get("general")
    #
    # word = word
    # news_part_start_date = news_part_data_dict.get("data").get("index")[0].get("startDate")
    # news_part_end_state = news_part_data_dict.get("data").get("index")[0].get("endDate")
    # news_part_data = decrypt(map_list, news_part)
    # news_part_general_data = decrypt(map_list, news_part_end_state)


    # 获取资讯指数的所有数据
    news_all_base_url = "https://index.baidu.com/api/FeedSearchApi/getFeedIndex?"
    news_all_params = {
        "area": 0,
        "word": word
    }
    news_all_url = news_all_base_url + urllib.parse.urlencode(news_all_params)
    news_all_response = s.get(news_all_url)
    time.sleep(3)
    news_all_data_dict = json.loads(news_all_response.text)
    if not news_all_data_dict.get("data"):
        return None

    ptbk_base_url = "https://index.baidu.com/Interface/ptbk?uniqid={}"
    uniqid = news_all_data_dict.get("data").get("uniqid")
    ptbk_url = ptbk_base_url.format(uniqid)
    ptbk_response = s.get(ptbk_url)
    time.sleep(3)
    # 映射表的原始数据
    map_list = json.loads(ptbk_response.text).get("data")

    news_all_general = news_all_data_dict.get("data").get("index")[0].get("general")
    news_all = news_all_data_dict.get("data").get("index")[0].get("data")


    word = word
    index_type = "news"
    news_all_start_date = news_all_data_dict.get("data").get("index")[0].get("startDate")
    news_all_end_date = news_all_data_dict.get("data").get("index")[0].get("endDate")
    data_type = news_all_data_dict.get("data").get("index")[0].get("type")
    news_all = decrypt(map_list, news_all)

    item = {
        "word": word,
        "index_type": index_type,
        "data": news_all,
        "start_date": news_all_start_date,
        "end_date": news_all_end_date,
        "data_type": data_type
    }
    return item


def crawl_media(s, word):
    print("media")
    word = word.replace("（", "").replace("）", "").strip()
    # media_part_base_url = "https://index.baidu.com/api/NewsApi/getNewsIndex?&startDate=2019-01-30&endDate=2019-02-28&days=30"
    # media_part_params = {
    #     "area": 0,
    #     "word": word,
    #     "startDate": "2019-01-30",
    #     "endDate": "2019-02-28",
    #     "days": 30
    # }
    # media_part_url = media_part_base_url + urllib.parse.urlencode(media_part_params)
    # media_part_response = s.get(media_part_url)
    # media_part_data_dict = json.loads(media_part_response.text)
    # if not media_part_data_dict.get("data"):
    #     return None
    # media_part = media_part_data_dict.get("data").get("index")[0].get("data")
    # media_part_general = media_part_data_dict.get("data").get("index")[0].get("general")

    # ptbk_base_url = "https://index.baidu.com/Interface/ptbk?uniqid={}"
    # uniqid = media_part_data_dict.get("data").get("index")["uniqid"]
    # ptbk_url = ptbk_base_url.format(uniqid)
    # ptbk_response = s.get(ptbk_url)
    # 映射表的原始数据
    # map_list = json.loads(ptbk_response.text).get("data")

    media_all_base_url = "https://index.baidu.com/api/NewsApi/getNewsIndex?area=0&word=%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6"
    media_all_params = {
        "area": 0,
        "word": word
    }
    media_all_url = media_all_base_url + urllib.parse.urlencode(media_all_params)
    media_all_response = s.get(media_all_url)
    time.sleep(3)
    media_all_data_dict = json.loads(media_all_response.text)
    if not media_all_data_dict.get("data"):
        return None

    ptbk_base_url = "https://index.baidu.com/Interface/ptbk?uniqid={}"
    uniqid = media_all_data_dict.get("data").get("uniqid")
    ptbk_url = ptbk_base_url.format(uniqid)
    ptbk_response = s.get(ptbk_url)
    time.sleep(3)
    # 映射表的原始数据
    map_list = json.loads(ptbk_response.text).get("data")

    media_all = media_all_data_dict.get("data").get("index")[0].get("data")
    media_all_general = media_all_data_dict.get("data").get("index")[0].get("general")

    word = word
    index_type = "media"
    media_all_data = decrypt(map_list, media_all)
    media_all_start_date = media_all_data_dict.get("data").get("index")[0].get("startDate")
    media_all_end_date = media_all_data_dict.get("data").get("index")[0].get("endDate")
    media_all_type = media_all_data_dict.get("data").get("index")[0].get("type")

    item = {
        "word": word,
        "index_type": index_type,
        "data": media_all_data,
        "start_date": media_all_start_date,
        "end_date": media_all_end_date,
        "data_type": media_all_type
    }
    return item


def decrypt(map_list, origin_data):
    """
    解密数据
    :return:
    """
    # map_list = "htUvQd63wg.-Klf47+,%038156-.29"
    # origin_data = "thdvthhv.t6v.fgv.ltv.wtvhtwvgtlvtl3v.3dv.h3v.fdvtlgvtf6v3d.v3dwvt.3v.thv..lvtfhv3dtvt6fvt3lvtg6vthlvtwwv3lhv3hfvtt6vtff"
    d = dict(zip(map_list[: len(map_list)//2], map_list[len(map_list)//2:]))
    # print(d)
    # print("".join(map(lambda x: d[x], origin_data)))
    return "".join(map(lambda x: d[x], origin_data))


if __name__ == '__main__':
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client["campus"]
    collection = db["school_index_0_500"]
    # get_cookie()
    s = login()
    with open("baidu_index/school_names.txt", "r") as f:
        words = f.readlines()

    for word in words[279:500]:

        # 此处正则 处理major的名字，例如：工程管理（注：可授管理学或工学学士学位）==》工程管理
        # if "（" in word:
        #     pattern = re.compile("(.+)（")
        #     word = pattern.match(word).group(1)

        search_item = crawl_search(s, word)
        # print(search_item)
        if search_item:
            collection.insert_one(dict(search_item))

        news_item = crawl_news(s, word)
        # print(news_item)
        if news_item:
            collection.insert_one(dict(news_item))

        media_item = crawl_media(s, word)
        # print(media_item)
        if media_item:
            collection.insert_one(dict(media_item))

        print(word)
    client.close()
