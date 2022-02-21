import sqlite3
import flask

def upd_user(user):
    conn = sqlite3.connect('ch3.db')
    print("Opened DB Successfully.")
    cur = conn.cursor()
    cur.execute("SELECT * from users where id=?;", (user['id'],))
    data = cur.fetchall()
    print(data)
    if len(data) == 0:
        flask.abort(404)
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
        return flask.jsonify(a_dict), 200
    else:
        conn.close()
        flask.abort(404)


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

    return flask.jsonify({'user_list': api_list}), 200

def add_user(new_user):
    conn = sqlite3.connect('ch3.db')
    print("Opened DB Successfully.")
    api_list = []
    cur = conn.cursor()
    cur.execute("SELECT * from users where username=? OR emailid=?", (new_user['username'], new_user['email']))
    data = cur.fetchall()
    if len(data) != 0:
        flask.abort(409)
    else:
        cur.execute(
            "INSERT INTO users (username, emailid, password, full_name) values (?,?,?,?);",
            (new_user['username'], new_user['email'], new_user['password'], new_user['name'])
                    )
        conn.commit()
        return "Success"
    conn.close()
    return flask.jsonify(new_user)


def del_user(user):
    conn = sqlite3.connect('ch3.db')
    print("Open database successfully.")
    cur = conn.cursor()
    cur.execute("SELECT * from users where username=?;",(user,))
    data = cur.fetchall()
    print("Data", data)
    if len(data) == 0:
        flask.abort(404)
    else:
        cur.execute("DELETE from users where username==?",(user,))
        conn.commit()
    return "Success."

    return "Success"