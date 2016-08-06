# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import MySQLdb

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '123456',
    'db': 'citest',
    'charset': 'utf8'
}
db = MySQLdb.connect(**config)
cursor = db.cursor()

app = Flask(__name__)
app.config.from_object('config')

@app.before_request
def before_request():
    #app.logger.info('before request started')
    pass

@app.teardown_request
def teardown_request(exception):
    #app.logger.info('teardown request')
    pass

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session['username'] == None:
            abort(401)
        return func(*args, **kwargs)

    return decorated_function

@app.errorhandler(401)
def page_forbid(error):
    app.logger.info(u'无权限')
    return render_template('401.html'), 401

@app.route('/')
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    count = cursor.execute('select * from t_user where username=%s and password=%s', (username, password))
    if count == 1:
        flash(u'登录成功')
        session['username'] = cursor.fetchone()[1]
        return redirect('/user/list')

    error_tip = u'用户名或密码错误'
    return render_template('login.html', error_tip=error_tip)

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect('/login')

@app.route('/user/list')
@login_required
def user_list():
    cursor.execute('select * from t_user limit 10')
    users = [dict(id=row[0], username=row[1], password=row[2], create_date=row[3]) for row in cursor.fetchall()]

    '''
    results = cursor.fetchall()
    users = []
    for row in results:
        id = row[0]
        username = row[1]
        password = row[2]
        create_date = row[3]
        user = {'id': id, 'username': username, 'password': password, 'create_date': create_date}
        users.append(user)
    '''

    return render_template('user-list.html', users=users)

@app.route('/user/new', methods=['GET'])
def user_new():
    return render_template('user-new.html')

@app.route('/user/create', methods=['POST'])
def user_create():
    username = request.form['username']
    password = request.form['password']
    cursor.execute('insert into t_user(username, password, create_date) values(%s,%s,current_timestamp())', (username, password))
    flash(u'创建成功')
    return redirect('/user/list')

@app.route('/user/<user_id>')
def user_show(user_id):
    cursor.execute('select * from t_user where id=%s', (user_id,))
    row = cursor.fetchone()
    id = row[0]
    username = row[1]
    password = row[2]
    create_date = row[3]
    user = {'id': id, 'username': username, 'password': password, 'create_date': create_date}

    return render_template('user-show.html', user=user)

@app.route('/json')
def json_show():
    user = {'id': 1, 'username': u'中文名字', 'pasword': '123456'}
    #return jsonify(user=user)
    return jsonify(user)

@app.route('/user/delete/<user_id>')
def user_delete(user_id):
    cursor.execute('delete from t_user where id=%s', (user_id))
    flash(u'删除成功')
    return redirect('/user/list')

if __name__ == '__main__':
    app.run()
