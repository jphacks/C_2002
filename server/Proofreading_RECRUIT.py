# -*- coding: utf-8 -*-
import os
import configparser
import requests

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
def run_roofreading(sentence):
    # Proofreading APIへのGET通信
    response_proofreading = requests.get(RECRUITE_API_PROOFREADING_URL + '?apikey=' + RECRUITE_API_PROOFREADING_API_KEY + '&sentence=' + sentence)
    return response_proofreading.text

sentence = "システムの企画から開発・運用まで幅広く関われまs。"
# sentence = "システムの規格から開発・運用まで幅広く関われます。"

# 校正支援をJSON形式で取得
result_calibration_json = run_roofreading(sentence)
result_calibration_json = {
    'calibration': result_calibration_json
}
res = requests.post('http://localhost:5000/test', result_calibration_json, headers)
print(res)