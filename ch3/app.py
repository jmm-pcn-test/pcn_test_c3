from time import strftime, gmtime

from flask import Flask, jsonify, make_response, abort, request, render_template, redirect, url_for, session
from flask_cors import CORS, cross_origin
import json
import sqlite3

import v1
import v2

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/addname')
def addname():
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        return redirect(url_for('main'))
    else:
        return render_template('addname.html', session=session)

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('main'))

@app.route('/set_cookie')
def cookie_insertion():
    redirect_to_main = redirect('/')
    response = app.make_response(redirect_to_main)
    response.set_cookie('cookie_name',value='values')

    return response

@app.route("/adduser")
def adduser():
    return render_template("adduser.html")

@app.route('/addtweets')
def addtweet():
    return render_template("addtweets.html")


@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect('ch3.db')
    print("Opened DB Successfully.")
    api_list=[]
    fields = ('buildtime', 'version', 'methods', 'links')
    # cur = conn.execute("SELECT buildtime, version, methods, links from apirelease")
    # q = "SELECT %s, %s, %s, %s from apirelease;" % fields
    # print(q)
    cur = conn.execute("SELECT %s, %s, %s, %s from apirelease;" % fields)

    for row in cur:
        # a_dict = {}
        a_dict = {fields[idx]:row[idx] for idx in range(len(fields))}
        api_list.append(a_dict)

    conn.close()
    return jsonify({'api_version':api_list}), 200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return v1.list_users()

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return v1.list_user(user_id)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    req = request.json
    if not req or not 'username' in req or not 'email' in req or not 'password' in req:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name',""),
        'password': request.json['password']
    }
    return jsonify({'status': v1.add_user(user)}), 201

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
        abort(400)
    user['id'] = user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print(user)
    return jsonify({'status': v1.upd_user(user)}), 200


@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = request.json['username']
    return jsonify({'status': v1.del_user(user)}), 200

@app.route('/api/v2/tweets',methods=['GET'])
def  get_tweets():
    return v2.list_tweets(), 200

@app.route('/api/v2/tweets/<int:id>',methods=['GET'])
def  get_tweet(id):
    return v2.list_tweet(id), 200

@app.route('/api/v2/tweets', methods=['POST'])
def tweet_route():
    req = request.json
    if not req or not 'username' in req or not 'body' in req:
        abort(400)
    tweet = {
        'username':req['username'],
        'body':req['body'],
        'created_at': strftime("%Y-%m-%dT%H:%H:%SZ", gmtime())
    }
    return jsonify({"status": v2.add_tweet(tweet)}), 201

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error':'Resource not found!'}), 404)

@app.errorhandler(400)
def resource_not_found(error):
    return make_response(jsonify({'error':'Bad Request!'}), 400)

@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error':'Conflict! Record Exists.'}), 409)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

