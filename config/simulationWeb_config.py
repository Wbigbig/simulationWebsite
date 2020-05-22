#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/12/30 16:02
# Author  : W 
# FileName: simulationWeb_config.py
from datetime import timedelta

JSON_AS_ASCII = False   # 解决编码问题
SECRET_KEY = "Web"      # 设置token 生成salt

port = 6031

host = "0.0.0.0"

daemon = True

# HTML 模板热更新，主程序配合app.jinja_env.auto_reload = True
TEMPLATES_AUTO_RELOAD = True
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)

# 数据库连接
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Woshinidie123.@localhost:3306/simulation_web?charset=utf8"
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:rootpwd@127.0.0.1:3306/simulation_web?charset=utf8"