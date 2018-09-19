from flask import Flask, request, abort
from spider.screen_shot import Screen_Shot

app = Flask(__name__)

ss = Screen_Shot()

@app.route('/')
def index():
    return '<h1>Hello Spider!</h1>'

@app.route('/screen_shot', methods=['GET','POST'])
def shot_screen():
    if request.method == 'GET':
        abort('404')
    else:
        keyword = request.json['keyword']
        result = ss.run(keyword)
        return '<h1>%s</h1>' % result



if __name__ == '__main__':
    app.run(debug=True)
