# __author_="gLinlf"
# coding=utf-8
from flask import Flask

# 初始化文件
app = Flask(__name__)
# global pip
# app.config.from_object('config')
#  from .views import UserInfoView, SpiderView需要放在 app实例化后import 否则不能导入
from .views import UserInfoView, SpiderView, AdminView
