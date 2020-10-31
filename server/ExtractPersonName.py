# -*- coding:utf-8 -*-

import os
import urllib.request
import json
import configparser
import codecs
from goolabs import GoolabsAPI


if __name__ == '__main__':
    # ソースファイルの場所取得
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    # 設定値取得
    config = configparser.ConfigParser()
    config.read(APP_ROOT + '/config_local.ini')
    APPLICATION_ID = config.get("Goo_API", "ApplicationId")

    api = GoolabsAPI(APPLICATION_ID)
    #テキストファイルを読み込見たいとき
    text = open(APP_ROOT + "/sample.txt", "r", encoding="utf-8").read().replace('\n','')
    # response = api.entity(sentence="鈴木さんが今日の9時30分に横浜に行きます。")
    response = api.entity(sentence=text)
    people_name = [people[0] for people in response['ne_list'] if people[1]=='PSN']
    # print(response)
    print(people_name)