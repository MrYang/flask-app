### flask-web-app

创建flask 环境

1. `virtualenv flask` 创建flask 虚拟环境
2. `source flask/bin/activate` 激活flask 环境
3. `flask/bin/pip install -r requirements.txt` 安装python依赖
4. `deactivate` 退出当前python虚拟机环境


`gunicorn -b 127.0.0.1:8080 wsgi:application` 或者 `python views.py` 即可直接运行
