# -*- coding:utf-8 -*-

import os
import configparser
from goolabs import GoolabsAPI
import json
import requests


# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからgooラボAPIに関する情報を取得
Goo_API_APPLICATION_ID = config.get("Goo_API", "ApplicationId")

# gooラボAPIのAPIクライアント設定
gooAPI = GoolabsAPI(Goo_API_APPLICATION_ID)
#テキストファイルを読み込見たいとき
text = open(APP_ROOT + "/sample.txt", "r", encoding="utf-8").read().replace('\n','')
# response = gooAPI.entity(sentence="鈴木さんが今日の9時30分に横浜に行きます。")
response = gooAPI.entity(sentence=text)
people_name = set([people[0] for people in response['ne_list'] if people[1]=='PSN'])
companies_name = set([company[0] for company in response['ne_list'] if company[1]=='ORG'])
# print(response)
print(people_name)
print(companies_name)
result = {
    'people_name': people_name,
    'companies_name': companies_name
}
headers= {
    "Content-type": "application/json"
}

# print(json.dumps(result, indent=2))
# res = requests.post('http://localhost:5000/test', result)

res = requests.post('http://localhost:5000/test', result, headers)
print(res)