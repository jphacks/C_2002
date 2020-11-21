import os
import configparser
from goolabs import GoolabsAPI
import json
import re

# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからgooラボAPIに関する情報を取得
Goo_API_APPLICATION_ID = config.get("Goo_API", "ApplicationId")

# gooラボAPIのAPIクライアント設定
gooAPI = GoolabsAPI(Goo_API_APPLICATION_ID)

## 元のテキストデータ
f = open(APP_ROOT + '/before.txt', 'r', encoding='UTF-8')


## 辞書データ取得
json_open = open(APP_ROOT + '/dict.json', 'r')
HumbleLangDict = json.load(json_open)

## 名詞用辞書データ取得
json_open = open(APP_ROOT + '/noun.json', 'r')
HumbleNounDict = json.load(json_open)

# 探索の省略が可能な品詞（Part of speech to omit）
Posto = ['句点', '読点', '空白', '格助詞', '終助詞', '括弧', '助数詞', '助助数詞', '冠数詞']


## 形態素解析のデータを敬語に変換する関数
# def DataConverter(sentence):
#     # 探索の省略が可能な品詞（Part of speech to omit）
#     Posto = ['句点', '読点', '空白', '格助詞', '終助詞', '括弧', '助数詞', '助助数詞', '冠数詞']

#     ## 変換が必要な箇所を探索する
#     for start in range(len(sentence)):
#         ## 名詞の敬語に変換
#         # ひとつ前に冠名詞がないか確認
#         if start > 0 and sentence[start - 1][1] != '冠名詞':
#             # 品詞の確認
#             if sentence[start][1] == '名詞':
#                 # 名詞用辞書に登録されているか確認
#                 if sentence[start][0] in HumbleNounDict:
#                     # 辞書に登録されていれば敬語に変換
#                     sentence[start][0] = HumbleNounDict[sentence[start][0]]

#         ## 名詞以外を警護に変換
#         # 探索する必要がある品詞か判定
#         if sentence[start][1] not in Posto or re.search(r'(\W)', sentence[start][1]) == 'None':
#             # 辞書にヒットする語句を探索
#             for end in range(len(sentence) - 1, start - 1, -1):
#                 testKey = ''
#                 # 辞書の検索にかける文字列の生成
#                 for check in range(start, end + 1):
#                     testKey += sentence[check][0]
#                 # 文字列が辞書に登録されているか確認
#                 if testKey in HumbleLangDict:
#                     # 辞書に登録されていた敬語に文字列を変換する
#                     for i in range(start, end):
#                         sentence[i][0] = ""
#                     sentence[end][0] = HumbleLangDict[testKey]

#     # 形態素解析のデータを敬語に変換したものを返す
#     return sentence


## 敬語変換関数
# def ChangeToHonorific(original):
#     # See sample response below.
#     response = gooAPI.morph(sentence = original)

#     # 形態素解析のデータの抽出
#     originalData = response['word_list'][0]
#     # print(originalData)

#     # 形態素解析のデータを敬語に変換する関数の呼び出し
#     ConvertedData = DataConverter(originalData)

#     # 形態素解析のデータを敬語に変換したものを文に整形
#     ConvertedSentence = ""
#     for word in ConvertedData:
#         ConvertedSentence += word[0]
#     # 整形したデータを返す
#     return ConvertedSentence

def ChangeToHonorific(original):
    # See sample response below.
    response = gooAPI.morph(sentence = original)

    # 形態素解析のデータの抽出
    originalData = response['word_list'][0]
    # print(originalData)

    # # 形態素解析のデータを敬語に変換する関数の呼び出し
    # ConvertedData = DataConverter(originalData)
    ## 変換が必要な箇所を探索する
    for start in range(len(originalData)):
        ## 名詞の敬語に変換
        # ひとつ前に冠名詞がないか確認
        if start > 0 and originalData[start - 1][1] != '冠名詞':
            # 品詞の確認
            if originalData[start][1] == '名詞':
                # 名詞用辞書に登録されているか確認
                if originalData[start][0] in HumbleNounDict:
                    # 辞書に登録されていれば敬語に変換
                    originalData[start][0] = HumbleNounDict[originalData[start][0]]

        ## 名詞以外を警護に変換
        # 探索する必要がある品詞か判定
        if originalData[start][1] not in Posto or re.search(r'(\W)', originalData[start][1]) == 'None':
            # 辞書にヒットする語句を探索
            for end in range(len(originalData) - 1, start - 1, -1):
                testKey = ''
                # 辞書の検索にかける文字列の生成
                for check in range(start, end + 1):
                    testKey += originalData[check][0]
                # 文字列が辞書に登録されているか確認
                if testKey in HumbleLangDict:
                    # 辞書に登録されていた敬語に文字列を変換する
                    for i in range(start, end):
                        originalData[i][0] = ""
                    originalData[end][0] = HumbleLangDict[testKey]

    # 形態素解析のデータを敬語に変換したものを返す
    ConvertedData = originalData

    # 形態素解析のデータを敬語に変換したものを文に整形
    ConvertedSentence = ""
    for word in ConvertedData:
        ConvertedSentence += word[0]
    # 整形したデータを返す
    return ConvertedSentence

# テスト用に一行ずつ文を渡す
while True:
    original = f.readline()
    if original:
        ConvertedSentence = ChangeToHonorific(original)
        print('converted = ' + ConvertedSentence)   
    else:
        print('fin')
        break
f.close()