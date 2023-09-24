from flask import Flask, request, jsonify
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return super().default(obj)

app = Flask(__name__)
app.id_count     = 1
app.users        = {}
app.tweets       = []
app.json_encoder = CustomJSONEncoder

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user                = request.json
    new_user["id"]          = app.id_count
    app.users[app.id_count] = new_user
    app.id_count            = app.id_count + 1

    return jsonify(new_user)

@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet   = payload['tweet']

    if user_id not in app.users:
        return '유저가 존재 하지 않습니다', 400

    if len(tweet) > 300:
        return '300자를 초과했습니다', 400

    user_id = int(payload['id'])

    app.tweets.append({
        'user_id' : user_id,
        'tweet'   : tweet
    })

    return '', 200

@app.route('/follow', methods=['POST'])
def follow():
    payload           = request.json
    user_id           = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return '유저가 존재 하지 않습니다', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)

    return jsonify(user)

@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload           = request.json
    user_id           = int(payload['id'])
    user_id_to_follow = int(payload['unfollow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return '유저가 존재 하지 않습니다', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).discard(user_id_to_follow)

    return jsonify(user)

@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return '유저가 존재 하지 않습니다', 400

    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        'user_id'  : user_id,
        'timeline' : timeline
    })

if __name__ == '__main__':
    app.run(debug=True)


'''
running 했는데,
[Running] python -u "c:\python\repos\FlaskAPITest\ch05\timeline_example.py"
Traceback (most recent call last):
  File "c:\python\repos\FlaskAPITest\ch05\timeline_example.py", line 2, in <module>
    from flask.json import JSONEncoder
ImportError: cannot import name 'JSONEncoder' from 'flask.json' (C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\json\__init__.py)

PS C:\python\repos\FlaskAPITest\ch05> flask --version
Python 3.11.4 
Flask 2.3.3   
Werkzeug 2.3.7
이렇게 떠서 위와 같이 수정했다.
'''
