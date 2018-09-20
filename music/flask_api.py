from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello Music!</h1>'

@app.route('/music', methods=['POST'])
def get_music():
        return '<h1>%s</h1>' % '塔里的男孩'



if __name__ == '__main__':
    app.run(debug=True)
