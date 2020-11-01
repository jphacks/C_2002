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

# JSON送信用のヘッダー
headers= {
    "Content-type": "application/json"
}

# gooラボAPIのAPIクライアント設定
gooAPI = GoolabsAPI(Goo_API_APPLICATION_ID)

# 人名と会社名をJSON形式で取得する関数
def get_json_people_companies(sentence):
    response = gooAPI.entity(sentence=sentence)
    people_name = list(set([people[0] for people in response['ne_list'] if people[1]=='PSN']))
    companies_name = list(set([company[0] for company in response['ne_list'] if company[1]=='ORG']))
    return json.dumps(people_name, ensure_ascii=False), json.dumps(companies_name, ensure_ascii=False)

# テキストファイルを読み込見たいとき
sentence = open(APP_ROOT + "/sample.txt", "r", encoding="utf-8").read().replace('\n','')

# 人名と会社名をJSON形式で取得
people_name_json, companies_name_json = get_json_people_companies(sentence)
result = {
    'people_name': people_name_json,
    'companies_name': companies_name_json
}
res = requests.post('http://localhost:5000/test', result, headers)
print(res.text)