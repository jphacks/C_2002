import os
import configparser
from goolabs import GoolabsAPI
import json

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


# 元のテキストデータ
f = open(APP_ROOT + '/before.txt', 'r', encoding='UTF-8')
data = f.read()
OriginalText = data

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
       print(json.dumps(HumbleLangDict, indent=2).encode().decode('unicode-escape'))
       
       global HitWordList
       HitWordList = []

       # See sample response below.
       response = gooAPI.morph(sentence = text)
       # 文章ごとに変換
       for sentence in response['word_list']:
             SearchForWords(sentence)
       print(HitWordList)
       ConvertedText = ChangeWord(text, HitWordList)
       return ConvertedText

# 敬語変換関数呼び出し
ChangeText = ChangeToHonorific(OriginalText)
print(ChangeText)
print(OriginalText)
f.close()

# 結果をファイルに書き出す
path_w = APP_ROOT + '/result.txt'
with open(path_w, mode='w') as f:
    f.write(ChangeText)
f.close()