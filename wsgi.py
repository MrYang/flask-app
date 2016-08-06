# -*- coding: utf-8 -*-
from views import app

application = app

# gunicorn -b 127.0.0.1:8080 wsgi:application
if __name__ == '__main__':
    application.run()
