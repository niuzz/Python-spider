from flask import Flask, request, abort, make_response
from spider.screen_shot import Screen_Shot
import json
import requests
import threading

app = Flask(__name__)

ss = Screen_Shot()

lock = threading.Lock()

@app.route('/')
def index():
    return '<h1>Hello screen shot!</h1>'


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
                lock.acquire()
                try:
                    keyword = result[key]
                    img_result = ss.run(keyword, key)
                    if img_result:
                        img_arr.append(img_result)
                finally:
                    lock.release()

            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post('https://www.wangxinlong.top/http.php', data=json.dumps(img_arr), headers=headers)
            print(r.text)
            return json.dumps(img_arr)


if __name__ == '__main__':
    app.run(debug=True)
