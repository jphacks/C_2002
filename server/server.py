# coding: UTF-8

from flask import Flask, request
import os
import configparser
from goolabs import GoolabsAPI
import json
import requests
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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

# 人名と会社名をJSON形式で取得する関数
def get_json_people_companies(sentence):
    response = gooAPI.entity(sentence=sentence)
    people_name = list(set([people[0] for people in response['ne_list'] if people[1]=='PSN']))
    companies_name = list(set([company[0] for company in response['ne_list'] if company[1]=='ORG']))
    return people_name, companies_name

# 校正支援をJSON形式で取得する関数
def get_json_roofreading(text):
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

# ローカルGETテスト用
@app.route('/')
def hello():
    name = "Hello World"
    return name

# ローカルPOSTテスト用
@app.route('/test', methods=['POST'])
def post_test():
    # Node.jsからのPOST
    json_file = request.get_json()
    print(json_file['people_name'])
    print(json_file['companies_name'])

    # PythonからのPOST
    # print(request.form['people_name'])
    # print(request.form['companies_name'])
    return 'Success'

@app.route('/getdata')
def post_getdata():
    # テキストファイルの読み込み
    sentence = open(APP_ROOT + "/sample.txt", "r", encoding="utf-8").read().replace('\n','')

    # 人名と会社名をJSON形式で取得
    people_name_json, companies_name_json = get_json_people_companies(sentence)
    # 校正支援をJSON形式で取得
    result_calibration_json = get_json_roofreading(sentence)

    # 全て結果をJSON形式にまとめて返す
    result = {
        'people_name': people_name_json,
        'companies_name': companies_name_json,
        'calibration': result_calibration_json
    }
    return result

@app.route('/postdata', methods=['POST'])
def post_postdata():
    json_post = request.get_json()
    sentence = json_post['sentence'].replace('\n','')

    # 人名と会社名をJSON形式で取得
    people_name_json, companies_name_json = get_json_people_companies(sentence)
    # 校正支援をJSON形式で取得
    result_calibration_json = get_json_roofreading(sentence)
    # 全て結果をJSON形式にまとめて返す
    result = {
        'people_name': people_name_json,
        'companies_name': companies_name_json,
        'calibration': result_calibration_json
    }
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)