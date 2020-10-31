# coding: UTF-8

from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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

if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True)