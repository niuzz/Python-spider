from flask import Flask, request, abort, make_response
from spider.screen_shot import Screen_Shot
import json
import requests

app = Flask(__name__)

ss = Screen_Shot()


@app.route('/')
def index():
    return '<h1>Hello Spider!</h1>'


@app.route('/screen_shot', methods=['GET', 'POST'])
def shot_screen():
    if request.method == 'GET':
        abort('404')
    else:
        try:
            result = json.dumps(request.get_json())
        except:
            abort('400')
        else:
            result = json.loads(result)
            keys = result.keys()
            img_arr = []
            for key in keys:
                keyword = result[key]
                img_result = ss.run(keyword, key)
                if img_result:
                    img_arr.append(img_result)
                else:
                    img_arr.append(json.dumps({'type': 'None'}))
            return ''.join(img_arr)

if __name__ == '__main__':
    app.run(debug=True)
