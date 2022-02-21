from flask import Flask, jsonify, make_response, abort, request
import json
import sqlite3

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

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
    # print(api_list)
    # res = (jsonify({'api_version':api_list}), 200)
    # print(res)
    return jsonify({'api_version':api_list}), 200

@app.route('/api/v1/users', methods=['GET'])
def get_users():

    return list_users()

def list_users():
    conn = sqlite3.connect('ch3.db')
    print("Opened DB Successfully.")
    api_list = []
    fields = ('username', 'emailid', 'password', 'full_name', 'id')
    cur = conn.execute("SELECT %s, %s, %s, %s, %s from users;" % fields)

    for row in cur:
        # a_dict = {}
        a_dict = {fields[idx]:row[idx] for idx in range(len(fields))}
        api_list.append(a_dict)

    return jsonify({'user_list': api_list}), 200

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)


def list_user(user_id):
    conn = sqlite3.connect('ch3.db')
    print("Opened DB Successfully.")
    api_list = []
    cur = conn.cursor()
    cur.execute("SELECT * from users where id=?",(user_id,))
    data = cur.fetchall()

    fields = ('username', 'emailid', 'password', 'full_name', 'id')
    a_dict = {}
    if len(data) !=0:
        a_dict = {fields[idx]: data[0][idx] for idx in range(len(fields))}
        conn.close()
        return jsonify(a_dict), 200
    else:
        conn.close()
        abort(404)


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
    return jsonify({'status': add_user(user)}), 201

def add_user(new_user):
    conn = sqlite3.connect('ch3.db')
    print("Opened DB Successfully.")
    api_list = []
    cur = conn.cursor()
    cur.execute("SELECT * from users where username=? OR emailid=?", (new_user['username'], new_user['email']))
    data = cur.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        cur.execute(
            "INSERT INTO users (username, emailid, password, full_name) values (?,?,?,?);",
            (new_user['username'], new_user['email'], new_user['password'], new_user['name'])
                    )
        conn.commit()
        return "Success"
    conn.close()
    return jsonify(new_user)

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
    return jsonify({'status': upd_user(user)}), 200

def upd_user(user):
    conn = sqlite3.connect('ch3.db')
    print("Opened DB Successfully.")
    cur = conn.cursor()
    cur.execute("SELECT * from users where id=?;", (user['id'],))
    data = cur.fetchall()
    print(data)
    if len(data) == 0:
        abort(404)
    else:
        key_list = user.keys()
        for key in key_list:
            if key != 'id':
                print(user,key)
                cur.execute(
                    """UPDATE users SET {0} = ? WHERE id = ?""".format(key), (user[key],user['id'])
                )
                conn.commit()
        return "Success."


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

