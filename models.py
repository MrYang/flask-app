# -*- coding: utf-8 -*-

import time

class User:

    def __init__(self, id, username, password, create_date):
        self.id = id
        self.username = username
        self.password = password
        self.create_date = create_date

    def pp(self):
        print 'id:%s,username:%s,password:%s,create_date:%s' % (self.id, self.username, self.password, time.strftime('%Y-%m-%d %H:%M:%S', self.create_date))


if __name__ == '__main__':
    user = User(1, 'yxb', '123456', time.localtime())
    user.pp()
