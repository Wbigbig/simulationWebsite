#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/12/31 11:24
# Author  : W 
# FileName: run.py
import hmac
import sys
sys.path.append("..")

from __init__ import app,logger
# from __init__ import manager
from __init__ import login_manager, login_required, current_user, login_user, logout_user

from flask import render_template, redirect, url_for, request, flash, jsonify, current_app
from git.repo import Repo

import os
import traceback

from common.models import User
from common.forms import LoginForm, registerForm
from spyder.spyder51Job import Spyder51Job
from common.simple_decorators import user_required
from common import models

# 这个callback函数用于reload User object，根据session中存储的user id
# 提供user_loader的回调函数，主要是通过获取user对象存储到session中，自己实现最好启用缓存
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/github",methods=["POST"])
def github():
    """ Entry point for github webhook testkey"""
    logger.info("newnewnewcodenewcode")
    sha,signature = request.headers.get('X-Hub-Signature').split('=')
    logger.info(f'signature:{signature}'+ str(request.data))
    secret = str.encode(current_app.config.get('GITHUB_SECRET'))
    hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
    logger.info(f'hashhex:{hashhex}')
    if hmac.compare_digest(hashhex, signature):
        try:
            if 'GIT_DIR' in os.environ:
                del os.environ['GIT_DIR']
            logger.info('hash对比正确' + current_app.config.get('REPO_PATH'))
            logger.info("开始拉仓库")
            # repo = Repo(current_app.config.get('REPO_PATH'))
            repo = Repo("/usr/local/python3/graduate998/backStageNew")
            repo.git.pull()
            #---
            # origin = repo.remotes.origin
            # origin.pull()
            #---
            # 获取默认版本库 origin
            # remote = repo.remote()
            # 从远程版本库拉取分支
            # remote.pull()
            logger.info("pull操作完成了啊！")
            # commit = request.json['after'][0:6]
            # logger.info('Repository updated with commit {}'.format(commit))
        except:
            logger.info(traceback.format_exc())
            return jsonify({"error": str(traceback.format_exc())}),500
    return jsonify({}),200


@app.route("/register",methods=["GET","POST"])
def register():
    print("进来注册")
    form = registerForm()
    if form.validate_on_submit():
        phone = request.form.get('phone', None)
        name = request.form.get('name', None)
        pwd = request.form.get('pwd', None)
        valid = request.form.get('valid', None)
        valid2 = request.form.get('valid2', None)
        if valid == valid2:
            remember_me = request.form.get('remember_me', False)
            create = User.create_user(phone,name,pwd)
            if create["status"] == 200:
                user = User(phone)
                login_user(user, remember=remember_me)
                return redirect(url_for('main'))
            elif create["status"] == 401:
                flash(create["msg"])
            else:
                return redirect(url_for('login'))
        else:
            flash("验证码错误！")
    return render_template('register.html', title="register", form=form)

@app.route('/')
@app.route('/login',methods=["GET","POST"])
def login():
    print("进来登录了")
    form = LoginForm()
    if form.validate_on_submit():
        print("进来这个函数了")
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        print(user_name,password)
        user = User(user_name)
        if user.verify_password(password):
            print("进来储存用户啦")
            print(user.username,user.id)
            login_user(user, remember=remember_me)
            print("zheyibu")
            return redirect(url_for('main'))
        flash(u"用户名或密码错误！")
    return render_template('login.html', title="Sign In", form=form)

@app.route('/main')
@login_required
def main():
    print(current_user.name)
    return render_template(
        'index.html', name=current_user.name,phone=current_user.username,\
        job=current_user.job,experience=current_user.experience,age=current_user.age,sex=current_user.sex)

@app.route('/crud',endpoint="crud")
@login_required
def crud():
    return render_template(
        'crud.html', username=current_user.username)

@app.route('/getlist',endpoint="getlist")
# @user_required
@login_required
def getlist():
    print("进来拿数据了")
    return jsonify(Spyder51Job())

@app.route('/logout',endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # app.run(port=6031,host="0.0.0.0",debug=True)
    app.run()

