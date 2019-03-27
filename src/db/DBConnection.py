# __author_="gLinlf"
# coding=utf-8

import mongoengine

# 使用mongoengine 连接操作数据库
web_db_name = 'zhihu_data'
connection = mongoengine.connect('127.0.0.1', 27017)
con = connection.zhihu_data
db = con.user_info_data
db_f = con.following_url

