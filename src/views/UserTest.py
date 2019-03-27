# __author_="gLinlf"
# coding=utf-8

import os
import signal

from bson import ObjectId
from src.model.UserInfo import *
from src.db.DBConnection import *
from src.utils.CommUtils import CommUtils
from src.views.UserInfoView import show_business, show_schools

if __name__ == '__main__':
    # show_schools()

    all_985 = University985.objects.all()
    all_sch = []
    obj = {}
    print(all_985)
    t = db.find({'user_schools': {'$regex':'北京大学'}}).count()
    print('tt is ', t)
    for name in all_985:
        all_sch.append(name['univ_name'])

    for b in range(len(all_sch)):
        num = db.find({'user_schools': all_sch[b]}).count()
        if all_sch[b] == '':
            obj.update({"未知": num})
        else:
            obj.update({all_sch[b]: num})
    print(obj)


    def test_db(x):
        num = (x, db.find({'user_schools': x}).count())
        return num


    all_sch = db.distinct("user_schools")
    obj = {}
    print(all_sch)

    # ls = list(map(test_db, all_sch))
    # print(ls)

    # for b in range(len(all_sch)):
    #     num = db.find({'user_schools': all_sch[b]}).count()
    #     obj.update({all_sch[b]: num})
    #     print({all_sch[b]: num})

    # 对business_objs 的值（values）排序 取排行前20个行业
    objs_list = (sorted(CommUtils.dict2list(obj), key=lambda x: x[1], reverse=True))[0:20]
    # objs_list = (sorted(ls, key=lambda x: x[1], reverse=True))[0:20]
    print(objs_list)
    retn_keys = []
    retn_objs = {}
    for tup in objs_list:
        retn_keys.append(tup[0])
        retn_objs.update({tup[0]: tup[1]})
    print(retn_keys)
    print(retn_objs)


    # all_business = db.distinct("user_business")
    # business_objs = {}
    # # result.fromkeys(business)
    # for b in range(len(all_business)):
    #     num = db.find({'user_business': all_business[b]}).count()
    #     if all_business[b] == '':
    #         business_objs.update({"未知": num})
    #     else:
    #         business_objs.update({all_business[b]: num})
    # print(business_objs)
    # # 对business_objs 的值（values）排序 取排行前20个行业
    # objs_list = (sorted(CommUtils.dict2list(business_objs), key=lambda x: x[1], reverse=True))[0:20]
    # print(objs_list)
    # retn_keys = []
    # retn_objs = {}
    # for tup in objs_list:
    #     retn_keys.append(tup[0])
    #     retn_objs.update({tup[0]: tup[1]})
    # print(retn_keys)
    # print(retn_objs)

# def dict2list(dic: dict):
#         ''' 将字典转化为列表 '''
#         keys = dic.keys()
#         vals = dic.values()
#         lst = [(key, val) for key, val in zip(keys, vals)]
#         print(lst)
#         return lst
#
#
#     dic = {'a': 4, 'b': 2, 'c': 1, 'd': 5}
#     dic= sorted(dict2list(dic), key=lambda x: x[1], reverse=True)
#     print(dic)
#
#     test = show_business()

# b = db.runCommand({"distinct": "user_info_data", "key": "user_business"})
# business = db.distinct("user_business")
# result = {}
# # result.fromkeys(business)
# for b in range(len(business)):
#     num = db.find({'user_business':business[b]}).count()
#     result.update({business[b]:num})
# print(result)


# user_data = db.find().order_by({'user_followers': -1}).skip(0).limit(15)
# users = UserInfoData.objects.order_by('-user_followers').limit(10)
# print(type(users))
# print(users)
# print(type(user_data))
# y_data = []
# x_data = []
# for data in user_data:
#     print(data)
#     y_data.append(data['user_name'])
#     x_data.append(data['user_followers'])



print('')
# a = os.popen('taskkill /pid' + str(11528) + '-t -f')
# 分页10条
# datas = db.find().skip(0).limit(10)
# print(type(datas))
# for data in datas:
#     print(type(data))
#     js = json.dumps(str(data), ensure_ascii=False)
#     print(js)
#  通过Id查询信息
# user_info = db.find({'_id' : ObjectId('58d0c1cbf6f657337478c7d6')})
# for data in user_info:
#     print(data)

# 删除信息
# db.remove({'_id':ObjectId('58ce00f5f6f657352c4d1f0a')})
