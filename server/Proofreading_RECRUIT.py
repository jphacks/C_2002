# -*- coding: utf-8 -*-

import os
import configparser
import requests
import json

# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからRECRUITのAPIに関する情報を取得
RECRUITE_API_PROOFREADING_API_KEY = config.get("RECRUITE_API", "ProofreadingAPIKey")
RECRUITE_API_PROOFREADING_URL = config.get("RECRUITE_API", "ProofreadingURL")

# JSON送信用のヘッダー
headers= {
    "Content-type": "application/json"
}

# 校正支援をJSON形式で取得する関数
def get_json_roofreading(text):
    sentences = text.split('。')
    response_list = []
    result_list = []
    for sentence in sentences:
        # Proofreading APIへのGET通信
        response_proofreading = requests.get(RECRUITE_API_PROOFREADING_URL + '?apikey=' + RECRUITE_API_PROOFREADING_API_KEY + '&sentence=' + sentence)
        response_list.append(response_proofreading.json())
    # print(response_list)
    for res in response_list:
        if res['message']!='ok':
            result = {
                'inputSentence': res['inputSentence'],
                'checkedSentence': res['checkedSentence'],
                'alerts': res['alerts']
            }
            result_list.append(result)
    # return json.dumps(result_list, ensure_ascii=False)
    return result_list

sentence = "システムの企画から開発・運用まで幅広く関われまs。"
# sentence = "システムの規格から開発・運用まで幅広く関われます。"
# response_proofreading = requests.get(RECRUITE_API_PROOFREADING_URL + '?apikey=' + RECRUITE_API_PROOFREADING_API_KEY + '&sentence=' + sentence)
# print(response_proofreading.json())
# テキストファイルの読み込み
sentence = open(APP_ROOT + "/sample.txt", "r", encoding="utf-8").read().replace('\n','')

# 校正支援をJSON形式で取得
result_calibration_json = get_json_roofreading(sentence)
result_calibration_json = {
    'calibration': result_calibration_json
}
print(result_calibration_json)
# res = requests.post('http://localhost:5000/test', result_calibration_json, headers)
# print(res)