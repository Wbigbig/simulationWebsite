#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/11/12 16:14
# Author  : W 
# FileName: models.py
"""封装model类"""

from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import json
import time
import sys
from flask_sqlalchemy import SQLAlchemy
sys.path.append("..")
from __init__ import db

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.job = None
        self.experience = None
        self.age = None
        self.sex = None
        self.name = self.get_name()
        self.id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # @password.setter
    # def password(self, password):
    #     """save user name, id and password hash to json file"""
    #     self.password_hash = generate_password_hash(password)
    #     with open(PROFILE_FILE, 'w+') as f:
    #         try:
    #             profiles = json.load(f)
    #         except ValueError:
    #             profiles = {}
    #         profiles[self.username] = [self.password_hash,
    #                                    self.id]
    #         f.write(json.dumps(profiles))

    def verify_password(self, password):
        password_hash = self.get_password_hash()
        if not password_hash:
            return False
        if password == password_hash:
            print("密码正确")
            self.id = self.get_id()
            self.name = UserInfo.query.filter_by(id=self.id).first().name
            print(self.name)
            return True
        print("密码错误")
        return False

    def get_password_hash(self):
        """尝试从数据库获取密码：
        返回密码: 如果有该用户，则返回用户密码
        返回空：如果无对应用户，返回空
        """
        try:
            user = UserInfo.query.filter_by(phone=self.username).first()
            print(user)
            if user:
                return user.pwd
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_id(self):
        """
        从数据库中获取用户id
        """
        if self.username is not None:
            try:
                user = UserInfo.query.filter_by(phone=self.username).first()
                if user:
                    print("用户名存在",user)
                    self.job = user.job
                    self.experience = user.experience
                    self.age = user.age
                    self.sex = user.sex
                    return user.id
                print("找不到用户信息")
            except IOError:
                pass
            except ValueError:
                pass
        return None

    def get_name(self):
        """
        从数据库中获取用户name
        """
        if self.username is not None:
            try:
                user = UserInfo.query.filter_by(phone=self.username).first()
                if user:
                    print("用户名存在", user)
                    return user.name
                print("找不到用户信息")
            except IOError:
                pass
            except ValueError:
                pass
        return None

    @staticmethod
    def create_user(phone,name,pwd):
        if UserInfo.query.filter_by(phone=phone).first():
            return {"status": 401,"msg": "该手机已注册！"}
        if UserInfo.query.filter_by(name=name).first():
            return {"status": 401,"msg": "该昵称已存在！"}
        nowTime = int(time.time() * 1000)
        u1 = UserInfo(phone=phone, name=name, pwd=pwd, job=None, experience=None, create_time=str(nowTime))
        db.session.add(u1)
        db.session.commit()
        print("用户创建完成",phone,name,pwd)
        return {"status": 200,"msg": "成功！"}

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        try:
            print(user_id)
            return User(UserInfo.query.filter_by(id=user_id).first().phone)
        except:
            return None

class UserInfo(db.Model):
    __tablename__ = "user"
    # __table_args__ = {
    #     "mysql_charset": "utf8"
    # }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    # test5 = db.Column(db.String(50))
    # test6 = db.Column(db.String(50))
    # test7 = db.Column(db.String(50))
    # test8 = db.Column(db.String(50))
    name = db.Column(db.String(20), unique=True, nullable=False)
    pwd = db.Column(db.String(30), nullable=False)
    age = db.Column(db.String(4))
    sex = db.Column(db.String(4))
    job = db.Column(db.String(30))
    experience = db.Column(db.String(10))
    email = db.Column(db.String(50))    # 新增字段 验证 migrate_update
    # test = db.Column(db.String(50))
    # test2 = db.Column(db.String(50))
    # test3 = db.Column(db.String(50))
    # test4 = db.Column(db.String(50))
    create_time = db.Column(db.String(15))


# db.drop_all()
# print("删除成功")
db.create_all()
print("表创建成功")

# import time
# nowTime = int(time.time()*1000)
# u1 = UserInfo(phone="16888888888", name="创世元勋", pwd="root", job="root", experience="999", create_time=str(nowTime))
# db.session.add(u1)
# db.session.commit()
# print("插入u1成功")

"""
class Student(db.Model):
    __tablename__ = 'students'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    sno = db.Column(db.String(8),primary_key=True)
    sid = db.Column(db.String(18),unique=True,nullable=False)
    sname = db.Column(db.String(20),unique=True,nullable=False)
    ssex = db.Column(db.String(4),nullable=False,default='未知')
    sbirth = db.Column(db.Date,nullable=False)
    sdept = db.Column(db.String(30),nullable=False)
    sspecial = db.Column(db.String(30),nullable=False)
    sclass = db.Column(db.String(30),nullable=False)
    saddr = db.Column(db.String(60),nullable=False)
    # rank = db.Column(db.String(10),nullable=False,default='0')
    # cfl = db.relationship('Card','FillInf','LosInf',backref='student')
    card = db.relationship('Card',backref='student')
    fillinf = db.relationship('FillInf',backref='student')
    losinf = db.relationship('LosInf',backref='student')

class Card(db.Model):
    __tablename__ = 'cards'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    cardno = db.Column(db.Integer,primary_key=True)
    sid = db.Column(db.String(18),nullable=False)
    # cardstyle = db.Column(db.String(10),nullable=False)
    cardstate = db.Column(db.String(10),default='不可用',nullable=False)
    cardmoney = db.Column(db.Float,default=0.00,nullable=False)
    # cardtime = db.Column(db.Time,nullable=False)
    sno = db.Column(db.String(8),db.ForeignKey('students.sno'))
    # fl = db.relationship('FillInf','LosInf',backref='card')
    fillinf = db.relationship('FillInf',backref='card')
    losinf = db.relationship('LosInf',backref='card')

# class CardCenter(db.Model):
#     __tablename__ = 'cardcenter'
#     ccno = db.Column(db.String(8),primary_key=True)
#     ccaddr = db.Column(db.String(50),nullable=False)
#     jbr = db.Column(db.String(10),nullable=False)

class FillInf(db.Model):
    __tablename__ = 'fillinf'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    czno = db.Column(db.Integer,primary_key=True)
    czrq = db.Column(db.Time,nullable=False)
    czje = db.Column(db.Integer,nullable=False)
    # jbr = db.Column(db.String(10),nullable=False)
    cardno = db.Column(db.Integer,db.ForeignKey('cards.cardno'))
    sno = db.Column(db.String(8),db.ForeignKey('students.sno'))

class LosInf(db.Model):
    __tablename__ = 'losinf'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    gsno = db.Column(db.Integer,primary_key=True)
    gsrq = db.Column(db.Time,nullable=False)
    jgrq = db.Column(db.Time,nullable=False)
    # jbr = db.Column(db.String(10),nullable=False)
    cardno = db.Column(db.Integer, db.ForeignKey('cards.cardno'))
    sno = db.Column(db.String(8), db.ForeignKey('students.sno'))
"""

