#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2020/4/1 14:20
# Author  : W 
# FileName: migrate_update.py

from flask_script import Manager #flask 脚本
from flask_migrate import Migrate,MigrateCommand #flask 迁移数据

from __init__ import db
from __init__ import app

from  common.models import UserInfo

manager = Manager(app)
#要使用flask-migrat 先绑定db和app
migrate = Migrate(app,db)
# 将MigrateCommand添加到manager中，"db"是自定义命令
manager.add_command("db",MigrateCommand)

# db.create_all()
# print("表创建成功")

if __name__ == '__main__':
    manager.run()