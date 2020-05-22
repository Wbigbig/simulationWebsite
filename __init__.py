#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/12/31 11:36
# Author  : W 
# FileName: __init__.py

from flask import Flask
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile("./config/simulationWeb_config.py")
app.jinja_env.auto_reload = True    # 模板热更新

with open('key.txt') as f:
    read_info = f.readlines()

app.config['GITHUB_SECRET'] = read_info[0].replace("\n", "")
app.config['REPO_PATH'] = read_info[1]

db = SQLAlchemy(app)

# use login manager to manage session 使用登录管理器管理会话
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'            #登录视图
login_manager.login_message = u"用户失效！"   #快闪消息
login_manager.init_app(app=app)

# csrf protection 开启csrf_token保护
# csrf = CSRFProtect()
# csrf.init_app(app)
#关闭 app.config['WTF_CSRF_ENABLED'] = False
