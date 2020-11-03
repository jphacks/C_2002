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

# 人名と会社名をリストで取得する関数
def get_list_people_companies(sentence):
    response = gooAPI.entity(sentence=sentence)
    people_name = list(set([people[0] for people in response['ne_list'] if people[1]=='PSN']))
    companies_name = list(set([company[0] for company in response['ne_list'] if company[1]=='ORG']))
    return people_name, companies_name

# 校正支援をリストで取得する関数
def get_list_roofreading(text):
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
def ChangeToHonorific(text):
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
    f = open(APP_ROOT + "/before.txt", "r", encoding="utf-8")
    sentence = f.read()
    commit_id = '1c40b98'

    # 人名と会社名をリストで取得
    people_name_list, companies_name_list = get_list_people_companies(sentence)
    # 校正支援をリストで取得
    result_before_text_calibration_list = get_list_roofreading(sentence)
    # 敬語変換
    change_text = ChangeToHonorific(sentence)
    # 敬語変換後の校正支援をリストで取得
    result_change_text_calibration_list = get_list_roofreading(change_text)

    # 全て結果をJSON形式にまとめて返す
    result = {
        'commit_id': commit_id,
        'before_sentence': sentence,
        'people_name_list': people_name_list,
        'companies_name_list': companies_name_list,
        'before_sentence_calibration': result_before_text_calibration_list,
        'change_sentence': change_text,
        'change_sentence_calibration': result_change_text_calibration_list
    }
    f.close()
    return result

@app.route('/postdata', methods=['POST'])
def post_postdata():
    json_post = request.get_json()
    print(json_post)
    commit_id = json_post['commit_id']
    sentence = json_post['sentence']
    
    # 人名と会社名をリストで取得
    people_name_list, companies_name_list = get_list_people_companies(sentence)
    # 校正支援をリストで取得
    result_before_text_calibration_list = get_list_roofreading(sentence)
    # 敬語変換
    change_text = ChangeToHonorific(sentence)
    # 敬語変換後の校正支援をリストで取得
    result_change_text_calibration_list = get_list_roofreading(change_text)
    
    # 全て結果をJSON形式にまとめて返す
    result = {
        'commit_id': commit_id,
        'before_sentence': sentence,
        'people_name_list': people_name_list,
        'companies_name_list': companies_name_list,
        'before_sentence_calibration': result_before_text_calibration_list,
        'change_sentence': change_text,
        'change_sentence_calibration': result_change_text_calibration_list
    }
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)