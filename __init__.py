#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/12/31 11:36
# Author  : W 
# FileName: __init__.py

from flask import Flask
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import logging.handlers



LOG_FILE = 'log.log'
# 实例化handler
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)

fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - [%(levelname)s] - %(message)s'

# 实例化formatter
formatter = logging.Formatter(fmt)
# 为handler添加formatter
handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)
# 获取名为tst的logger
logger = logging.getLogger('tst')
# 为logger添加handler
logger.addHandler(handler)
# logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

logger.info('first info message')
logger.debug('first debug message')

app = Flask(__name__)

app.config.from_pyfile("./config/simulationWeb_config.py")
app.jinja_env.auto_reload = True    # 模板热更新

with open('key.txt') as f:
    read_info = f.readlines()

logger.info(read_info[0].replace("\n", ""))
logger.info(read_info[1])
logger.info("reload")
logger.info("修复crud页******************************************push code test reload!###########################################")
logger.info("new code push!***************************")
logger.info("new code push!###########################")
logger.info("快要崩了啊兄弟！！！！！")
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
