# -*- coding:utf-8 -*-

import os
import configparser
from goolabs import GoolabsAPI
import json
import requests
import asyncio
import sys
import time
import re


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

# 人名と会社名をリストで取得する関数
async def get_list_people(sentence):
    loop = asyncio.get_event_loop()
    response = gooAPI.entity(sentence=sentence)
    people_name = list(set([people[0] for people in response['ne_list'] if people[1]=='PSN']))
    print(people_name)
    return people_name
# 人名と会社名をリストで取得する関数
async def get_list_companies(sentence):
    loop = asyncio.get_event_loop()
    response = gooAPI.entity(sentence=sentence)
    companies_name = list(set([company[0] for company in response['ne_list'] if company[1]=='ORG']))
    return companies_name

# 人名と会社名をリストで取得する関数
async def get_list_people_companies(sentence):
    loop = asyncio.get_event_loop()
    response = gooAPI.entity(sentence=sentence)
    people_name = list(set([people[0] for people in response['ne_list'] if people[1]=='PSN']))
    companies_name = list(set([company[0] for company in response['ne_list'] if company[1]=='ORG']))
    return people_name, companies_name

# 校正支援をリストで取得する関数
async def get_list_roofreading(text):
    sentences = re.split('[、。，．,.!！？?"「」]', text)
    response_list = []
    result_list = []
    for sentence in sentences:
        # Proofreading APIへのGET通信
        response_proofreading = requests.get(RECRUITE_API_PROOFREADING_URL + '?apikey=' + RECRUITE_API_PROOFREADING_API_KEY + '&sentence=' + sentence)
        response_list.append(response_proofreading.json())
    for res in response_list:
        if res['message']!='ok':
            result = {
                'inputSentence': res['inputSentence'],
                'checkedSentence': res['checkedSentence'],
                'alerts': res['alerts']
            }
            result_list.append(result)
    return result_list

# 単語探索関数
def SearchForWords(sentence):
    for start in range(len(sentence)):
        for end in range(len(sentence) - 1, start - 1, -1):
            testKey = ''
            for check in range(start, end + 1):
                testKey += sentence[check][0]
            if testKey in HumbleLangDict:
                if testKey not in HitWordList:
                    HitWordList.append(testKey)

# 単語置き換え用関数
def ChangeWord(text, HitWordList):
    ConvertedText = text
    for word in HitWordList:
        ConvertedText = ConvertedText.replace(word, HumbleLangDict[word])
    return ConvertedText

# 敬語変換関数
async def ChangeToHonorific(text):
    loop = asyncio.get_event_loop()
    # 辞書データ取得
    json_open = open(APP_ROOT + '/sample.json', 'r')
    global HumbleLangDict
    HumbleLangDict = json.load(json_open)
    # print(json.dumps(HumbleLangDict, indent=2).encode().decode('unicode-escape'))
       
    global HitWordList
    HitWordList = []

    # See sample response below.
    response = gooAPI.morph(sentence = text)
    # 文章ごとに変換
    for sentence in response['word_list']:
            SearchForWords(sentence)
    # print(HitWordList)
    ConvertedText = ChangeWord(text, HitWordList)
    return ConvertedText

array = [5, 1, 8, 3, 4]

loop = asyncio.get_event_loop()
sentence = '高尾と岡崎です。'

# print('=== 一つだけ実行してみよう ===')
# sentence = '高尾と岡崎です。'
# loop.run_until_complete(get_list_people(sentence))
# print(results)

print('\n=== 5つ並列的に動かしてみよう')
# gather = asyncio.gather(
#     get_list_people(sentence),
#     get_list_companies(sentence),
#     get_list_people(sentence),
#     get_list_people(sentence),
#     get_list_people(sentence)
# )
gather = asyncio.gather(
        get_list_people_companies(sentence),
        get_list_roofreading(sentence),
        ChangeToHonorific(sentence)
    )
results = loop.run_until_complete(gather)
print(results)