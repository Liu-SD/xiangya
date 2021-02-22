from flask import Flask, request, jsonify
from Report import json2pdf

app = Flask(__name__)


@app.route('/api/json2pdf', methods=['GET', 'POST'])
def index():
    content = request.json #request.json会自动将json数据转换成Python类型（字典或者列表）

    try:
        path = json2pdf(content)
    except IOError:
        return jsonify({"code":500, "msg": "\u6210\u529f", "link":""})

    # print(content['msg'])
    return jsonify({"code":200, "msg": "\u6210\u529f", "link":path})

if __name__ == '__main__':
    app.run()