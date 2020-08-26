from flask import Flask, jsonify, g
import pymysql


app = Flask(__name__)


@app.before_request
def before_request():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='haha', db='SocialMedia')
    g.db = conn


@app.after_request
def after_request(response):
    if g.db:
        g.db.close()
    return response


@app.route('/follow/<string:follower>/<string:followee>', methods=['POST'])
def follow(follower, followee):
    sql1 = "select users_id from users where name = '?';"
    sql2 = "select users_id from users where name = '?';"
    sql3 = "insert follow_relationship values (?,?)；"
    c = g.db.cursor()
    c.execute(sql1, followee)
    followee_id = str(c.fetchall()[0])
    c.execute(sql2, follower)
    follower_id = str(c.fetchall()[0])

    c.execute(sql3, (follower_id, followee_id))
    g.db.commit()


@app.route('/unfollow/<string:follower>/<string:followee>', methods=['DELETE'])
def unfollow(follower, followee):
    sql1 = "select users_id from users where name = '?';"
    sql2 = "select users_id from users where name = '?';"
    sql3 = "delete from follow_relationship where follower=?and followee=?;"
    c = g.db.cursor()
    c.execute(sql1, followee)
    followee_id = str(c.fetchall()[0])
    c.execute(sql2, follower)
    follower_id = str(c.fetchall()[0])

    c.execute(sql3, (follower_id, followee_id))
    g.db.commit()


@app.route('/get_follower/<string:user_name>', methods=['GET'])
def get_follower(user_name):
    sql1 = "select users_id from users where name = '?';"
    sql2 = "select name from users where users_id in (select follower from follow_relationship where followee = ?);"
    c = g.db.cursor()
    c.execute(sql1, user_name)
    followee_id = str(c.fetchone()[0])

    c.execute(sql2, followee_id)
    follower = c.fetchall()
    return jsonify(follower)


@app.route('/get_following/<string:user_name>/<int:page>', methods=['GET'])
def get_following(user_name, page): # page number starts from 0
    sql1 = "select users_id from users where name = '?';"
    sql2 = "select name from users where users_id in (select followee from follow_relationship where follower = ?) order by name;"
    c = g.db.cursor()
    c.execute(sql1, user_name)
    follower_id = str(c.fetchone()[0])

    c.execute(sql2, follower_id)
    following = c.fetchall()
    return jsonify(following[page * 20:page * 20 + 20])


if __name__ == '__main__':
    app.run()
