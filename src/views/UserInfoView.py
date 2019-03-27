# __author_="gLinlf"
# coding=utf-8
# 知乎用户信息操作

from bson import ObjectId
from src import app
from src.db.DBConnection import *
from src.utils.CommUtils import *
from src.views.BaseView import *
from src.model.UserInfo import *
from src.logs.Logger import logger
from src.views.params import education_data, business_data, school_data, gender_data


@app.route('/')
@allow_cross_domain
def hello_world():
    datas = db.find({})
    print(type(datas))
    for data in datas:
        print(data)
    return 'hello'


# 知乎用户信息
@app.route('/showUserInfo')
@allow_cross_domain
def get_user_info():
    user_name = request.args.get('user_name')
    badge_topic = request.args.get('badge_topic')
    logger.info('user_name is {0} ,badge_topic is {1}'.format(user_name, badge_topic))
    page = int(request.args.get('state'))
    limit_size = int(request.args.get('limit'))
    if CommUtils.check_params(page, limit_size):
        start = (page - 1) * limit_size
        if CommUtils.is_not_empty(user_name) and not CommUtils.is_not_empty(badge_topic):
            total_size = db.find({'user_name': user_name}).count()
            user_data = db.find({'user_name': user_name}).skip(start).limit(limit_size)
        elif not CommUtils.is_not_empty(user_name) and CommUtils.is_not_empty(badge_topic):
            total_size = db.find({'badge_topics': {'$regex': badge_topic}}).count()
            user_data = db.find({'badge_topics': {'$regex': badge_topic}}).skip(start).limit(limit_size)
        elif CommUtils.is_not_empty(user_name) and CommUtils.is_not_empty(badge_topic):
            total_size = db.find({'badge_topics': {'$regex': badge_topic}, 'user_name': user_name}).count()
            user_data = db.find({'badge_topics': {'$regex': badge_topic}, 'user_name': user_name}).skip(start).limit(
                limit_size)
        else:
            total_size = db.find({}).count()
            user_data = db.find().skip(start).limit(limit_size)
        print(type(user_data))
        data_list = []
        for data in user_data:
            # _id Objectid (不能序列化，转成json）？？
            data['_id'] = str(data['_id'])
            data_list.append(data)
        logger.info('第:{0} 页显示:{1} 条的用户信息:{2}'.format(page, limit_size, data_list))
        succ_dict = {'status': '000000', 'total': total_size, 'pageSize': limit_size, 'curPage': page,
                     'list': data_list}
        return jsonify(succ_dict)
    else:
        error_dict = {'status': '999999'}
        logger.info("参数传递有误！")
        return jsonify(error_dict)


# 查看具体用户明细
@app.route('/queryDetl')
@allow_cross_domain
def query_detail():
    _id = request.args.get("_id")
    data_list = []
    if CommUtils.check_params(_id):
        user_info = db.find({'_id': ObjectId(_id)})
        for data in user_info:
            data['_id'] = str(data['_id'])
            data['create_time'] = data['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            data_list.append(data)
        logger.info("用户:{0} 的所有明细信息:{1}".format(_id, data_list))
        return jsonify(data_list)
    else:
        logger.info('_id 为None ，获取用户详细信息失败！')
        return jsonify(data_list)


# 删除用户信息  获取post提交的参数
@app.route("/deleteInfo", methods=['post'])
@allow_cross_domain
def delete_info():
    print(type(request.form))
    # < class 'werkzeug.datastructures.ImmutableMultiDict'>
    _id = request.form["_id"]
    if CommUtils.check_params(_id):
        db.remove({'_id': ObjectId(_id)})
        logger.info("删除 {0} 成功！".format(_id))
        return jsonify([])
    else:
        logger.info('_id 为None ，删除用户详细信息失败!')
        return jsonify([])


# ----------------------------------------------数据分析 echart begin---------------------
# 回答问题数前15
@app.route("/showAnswers")
@allow_cross_domain
def show_answers():
    # 回答问题数前15
    status = '000000'
    # mongoengine 对原生sort（）方法不支持 使用order_by（）
    user_data = UserInfoData.objects.order_by('-user_answer_count').skip(0).limit(15)
    series_data = []
    x_data = []
    for data in user_data:
        x_data.append(data['user_name'])
        series_data.append(data['user_answer_count'])
    logger.info("问答问题数前15的用户:{0}和回答问题数:{1}".format(x_data, series_data))
    retn_data = {'status': status, 'data': series_data, 'xdata': x_data}
    return jsonify(retn_data)


# 粉丝数前15
@app.route("/showFollowers")
@allow_cross_domain
def show_followers():
    # 粉丝数排行前15
    status = '000000'
    # mongoengine 对原生sort（）方法不支持 使用order_by（）
    user_data = UserInfoData.objects.order_by('-user_followers').skip(0).limit(15)
    series_data = []
    y_data = []
    for data in user_data:
        y_data.append(data['user_name'])
        series_data.append(data['user_followers'])
    logger.info("粉丝前15的用户:{0}和粉丝数:{1}".format(y_data, series_data))
    retn_data = {'status': status, 'ydata': y_data, 'data': series_data}
    return jsonify(retn_data)


# 知乎赞同数前10 对应的感谢数和收藏数
@app.route("/showVotedMore")
@allow_cross_domain
def show_voted_more():
    # 粉丝数排行前15
    status = '000000'
    # mongoengine 对原生sort（）方法不支持 使用order_by（）
    user_data = UserInfoData.objects.order_by('-user_vote_up_count').skip(0).limit(10)
    x_data = []
    voted_data = []
    thanked_data = []
    favorite_data = []
    for data in user_data:
        x_data.append(data['user_name'])
        voted_data.append(data['user_vote_up_count'])
        thanked_data.append(data['user_thanked_count'])
        favorite_data.append(data['user_favorite_count'])
    series_data = {'votedData': voted_data, 'thankedData': thanked_data, 'favoriteData': favorite_data}
    logger.info("赞同数数前10的用户:{0}和对应的赞同数:{1}，感谢数:{2}，和收藏数:{3}".format(
        x_data, voted_data, thanked_data, favorite_data))
    retn_data = {'status': status, 'xdata': x_data, 'data': series_data}
    return jsonify(retn_data)


# 知乎关注数数前15
@app.route("/showFollowing")
@allow_cross_domain
def show_following():
    # 粉丝数排行前15
    status = '000000'
    # mongoengine 对原生sort（）方法不支持 使用order_by（）
    user_data = UserInfoData.objects.order_by('-user_following').skip(0).limit(15)
    series_data = []
    y_data = []
    for data in user_data:
        y_data.append(data['user_name'])
        series_data.append(data['user_following'])
    logger.info("关注数前15的用户:{0}和关注数:{1}".format(y_data, series_data))
    retn_data = {'status': status, 'ydata': y_data, 'data': series_data}
    return jsonify(retn_data)


# 性别比例情况
@app.route("/showGender")
@allow_cross_domain
def show_gender():
    if len(gender_data) == 0:
        man_count = db.find({'user_sex': 'man'}).count()
        female_count = db.find({'user_sex': 'female'}).count()
        none_count = db.find({'user_sex': 'none'}).count()
        retn_data = [{'value': man_count, 'name': '男'}, {'value': female_count, 'name': '女'},
                     {'value': none_count, 'name': '未知'}]
        gender_data.append(retn_data)
    else:
        retn_data = gender_data[0]
    return jsonify(retn_data)


# 行业分布情况
@app.route("/showBusiness")
@allow_cross_domain
def show_business():
    print('business_data :', business_data)
    if len(business_data) == 0:
        all_business = db.distinct("user_business")
        all_count = db.find({}).count()
        business_objs = {}
        # result.fromkeys(business)
        for b in range(len(all_business)):
            num = db.find({'user_business': all_business[b]}).count()
            if all_business[b] == '':
                business_objs.update({"未知": num})
            else:
                business_objs.update({all_business[b]: num})
        # 对business_objs 的值（values）排序 取排行前20个行业
        objs_list = (sorted(CommUtils.dict2list(business_objs), key=lambda x: x[1], reverse=True))[0:20]
        retn_keys = []
        retn_objs = []
        count = 0
        for tup in objs_list:
            retn_keys.append(tup[0])
            retn_objs.append({'name': tup[0], 'value': tup[1]})
            count = count + tup[1]
        # 剩余其他职业
        retn_keys.append('其他')
        other_count = all_count - count
        retn_objs.append({'name': '其他', 'value': other_count})
        logger.info("排行前20 的行业{0}".format(retn_keys))
        logger.info("排行前20 的行业 占比{0}".format(retn_objs))

        return_data = {'keysData': retn_keys, 'data': retn_objs}
        business_data.update(return_data)
    else:
        return_data = business_data
    return jsonify(return_data)


# 知乎用户受教育程度排行
# 985高效前20排名
@app.route("/showSchools")
@allow_cross_domain
def show_schools():
    status = '000000'
    if len(school_data) == 0:
        # all_sch = db.distinct("user_schools")
        all_985 = University985.objects.all()
        all_sch = []
        for name in all_985:
            all_sch.append(name['univ_name'])
        obj = {}
        count = 0
        for b in range(len(all_sch)):
            num = db.find({'user_schools': {'$regex': all_sch[b]}}).count()
            count = count + num
            if all_sch[b] == '':
                obj.update({"未知": num})
            else:
                obj.update({all_sch[b]: num})
        all_count = db.find({}).count()

        # 对business_objs 的值（values）排序 取排行前20个行业
        objs_list = (sorted(CommUtils.dict2list(obj), key=lambda x: x[1], reverse=True))[0:20]
        y_data = []
        series_data = []
        for tup in objs_list:
            y_data.append(tup[0])
            series_data.append(tup[1])
        logger.info('前二十的985大学排名{0}'.format(y_data))
        logger.info('前二十的985大学排名占比{0}'.format(series_data))
        retn_data = {'status': status, 'ydata': y_data, 'data': series_data}
        school_data.update(retn_data)
    else:
        retn_data = school_data
    return jsonify(retn_data)


# 知乎用户受教育程度排行
# 211高校人数占比
@app.route("/showEducation")
@allow_cross_domain
def show_education():
    status = '000000'
    # all_sch = db.distinct("user_schools")
    if len(education_data) == 0:
        all_211 = University211.objects.all()
        all_sch = []
        for name in all_211:
            all_sch.append(name['univ_name'])
        # 未填写
        all_sch.append('')
        sch211_count = 0
        sch_none = 0
        for b in range(len(all_sch)):
            num = db.find({'user_schools': {'$regex': all_sch[b]}}).count()
            if all_sch[b] == '':
                sch_none = sch_none + num
            else:
                sch211_count = sch211_count + num
        all_count = db.find({}).count()
        # 填写的其他大学
        sch_others = all_count - sch211_count - sch_none
        retn_keys = ['211高校', '其他学校', '未知学校']
        retn_objs = [{'name': '211高校', 'value': sch211_count}, {'name': '其他学校', 'value': sch_others},
                     {'name': '未知学校', 'value': sch_none}]
        retn_data = {'status': status, 'keysData': retn_keys, 'data': retn_objs}
        education_data.update(retn_data)
        logger.info('受教育程度返回值:{0}'.format(retn_data))
    else:
        retn_data = education_data

    return jsonify(retn_data)

# if __name__ == '__main__':
#     show_schools()
#     # 分页10条
#     datas = db.find().skip(0).limit(10)
#     print(type(datas))
#     for data in datas:
#         print(type(data))
#         js = json.dumps(str(data), ensure_ascii=False)
#         print(js)
#     # 通过Id查询信息
#     user_info = db.find({'_id': ObjectId('58d0c1cbf6f657337478c7d6')})
#     for data in user_info:
#         print(data)

# 删除信息


# app.run()
