# coding: UTF-8

from flask import Flask, request
import os
import configparser
from goolabs import GoolabsAPI
import json
import requests
import re
from flask_cors import CORS
import threading
from concurrent.futures import ThreadPoolExecutor


# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからgooラボAPIに関する情報を取得
Goo_API_APPLICATION_ID = config.get("Goo_API", "ApplicationId")
# 設定ファイルからRECRUITのAPIに関する情報を取得
RECRUITE_API_PROOFREADING_API_KEY = config.get("RECRUITE_API", "ProofreadingAPIKey")
RECRUITE_API_PROOFREADING_URL = config.get("RECRUITE_API", "ProofreadingURL")

# JSON送信用のヘッダー
headers= {
    "Content-type": "application/json"
}

# gooラボAPIのAPIクライアント設定
gooAPI = GoolabsAPI(Goo_API_APPLICATION_ID)


def pulus(x, y):
    sums = x + y
    return sums

# 人名と会社名をリストで取得する関数
def get_list_people_companies(sentence):
    response = gooAPI.entity(sentence=sentence)
    people_name = list(set([people[0] for people in response['ne_list'] if people[1]=='PSN']))
    print(people_name)
    companies_name = list(set([company[0] for company in response['ne_list'] if company[1]=='ORG']))
    print(companies_name)
    return people_name, companies_name

with ThreadPoolExecutor() as executor:
    x = range(5)
    y = range(5, 10)
    res = executor.submit(get_list_people_companies, '高尾と岡崎です。')


print(list(x))
print(list(y))
print(res.result())