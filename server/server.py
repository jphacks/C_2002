# coding: UTF-8

from flask import Flask, request, jsonify
import os
import configparser
from goolabs import GoolabsAPI
import json
import requests

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
    return json.dumps(people_name, ensure_ascii=False), json.dumps(companies_name, ensure_ascii=False)


@app.route('/')
def hello():
    name = "Hello World"
    return name

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

@app.route('/getdata', methods=['POST'])
def post_getdata():
    # Node.jsからのPOST
    json_file = request.get_json()
    print(json_file['people_name'])
    print(json_file['companies_name'])

    # PythonからのPOST
    # print(request.form['people_name'])
    # print(request.form['companies_name'])
    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)