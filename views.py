# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import MySQLdb
import json
from flask_sqlalchemy import SQLAlchemy

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '123456',
    'db': 'test',
    'charset': 'utf8'
}
db = MySQLdb.connect(**config)
cursor = db.cursor()

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, default='', nullable=False)
    password = db.Column(db.String, nullable=False)
    create_date = db.Column(db.DateTime)

    def __repr__(self):
        return "<User(id='%s', username='%s', password='%s', create_date='%s')>" % (
                                self.id, self.username, self.password, self.create_date)


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
def page_forbidden(error):
    app.logger.info(u'无权限')
    return redirect('/login')

@app.route('/')
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    count = User.query.filter_by(username = username).filter_by(password = password).count()
    if count == 1:
        flash(u'登录成功')
        session['username'] = username
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
    users = User.query.limit(10).all()

    return render_template('user-list.html', users=users)

@app.route('/user/new', methods=['GET'])
@login_required
def user_new():
    return render_template('user-new.html')

@app.route('/user/create', methods=['POST'])
@login_required
def user_create():
    username = request.form['username']
    password = request.form['password']
    cursor.execute('insert into t_user(username, password, create_date) values(%s,%s,current_timestamp())', (username, password))
    flash(u'创建成功')
    return redirect('/user/list')

@app.route('/user/<user_id>')
@login_required
def user_show(user_id):
    user = User.query.filter_by(id = user_id).first()

    return render_template('user-show.html', user=user)

@app.route('/json')
def json_show():
    user = {'id': 1, 'username': u'中文名字', 'pasword': '123456'}
    #return jsonify(user=user)
    return jsonify(user)

@app.route('/user/delete/<user_id>')
@login_required
def user_delete(user_id):
    cursor.execute('delete from t_user where id=%s', (user_id))
    flash(u'删除成功')
    return redirect('/user/list')

if __name__ == '__main__':
    app.run()