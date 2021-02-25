from flask import Flask, request, jsonify
# from Report import json2pdf
from Report import json2pdf

ip = "106.12.125.175" 
port = 12333

app = Flask(__name__, static_folder='./pdfs')


@app.route('/api/json2pdf', methods=['GET', 'POST'])
def index():
    content = request.json #request.json会自动将json数据转换成Python类型（字典或者列表）

    try:
        path = json2pdf(content, ip, port)
    except IOError:
        return jsonify({"code":500, "msg": "\u6210\u529f", "link":""})

    # print(content['msg'])
    return jsonify({"code":200, "msg": "\u6210\u529f", "link":path})

if __name__ == '__main__':
    # app.run()
    app.run(
        host = '0.0.0.0',
        port = port,  
        debug = True 
    )