import sqlite3

import flask

def list_tweets():
    conn = sqlite3.connect('ch3.db')
    api_lists = []
    cur = conn.execute('SELECT username, body, tweet_time, id from tweets;')
    data = cur.fetchall()
    conn.close()
    if len(data)>0:
        for row in data:
            tweets = {
                'Tweet By':row[0],
                'Body': row[1],
                'Timestamp': row[2],
                'id':row[3]
            }
            api_lists.append(tweets)
    else:
        return api_lists

    return flask.jsonify({'tweets_list':api_lists})


def list_tweet(id:int):
    conn = sqlite3.connect('ch3.db')
    cur = conn.execute('SELECT * from tweets where id=?;', (id))
    data = cur.fetchall()[0]
    conn.close()
    if len(data)>0:
        tweet = {
            'id':data[0],
            'username':data[1],
            'body':data[2],
            'tweet_time':data[3]
        }
    else:
        flask.abort(404)
    return flask.jsonify(tweet)


def add_tweet(tweet):
    conn = sqlite3.connect('ch3.db')
    cur = conn.execute('SELECT * from users where username=?;', (tweet['username']))
    data = cur.fetchall()

    if len(data) == 0:
        flask.abort(404)
    else:
        cur.execute(
            "INSERT into tweets (username, body, tweet_time) values (?,?,?);",
            (tweet['username'],tweet['body'], tweet['created_at'])
        )
        conn.commit()
    return "Success."