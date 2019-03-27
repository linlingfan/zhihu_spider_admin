# __author_="gLinlf"
# coding=utf-8

from datetime import datetime
import mongoengine
from src.db.DBConnection import web_db_name


# mongoengine.connect(web_db_name)


class UserInfoData(mongoengine.Document):
    # 用户信息地址
    user_url = mongoengine.StringField(default='')
    # 用户名
    user_name = mongoengine.StringField(default='')
    # 用户头像地址
    user_avatar_url = mongoengine.StringField(default='')
    # 用户标题简介
    user_head_line = mongoengine.StringField(default='')
    # 用户性别
    user_sex = mongoengine.StringField(default='')
    # 用户居住所在地
    user_locations = mongoengine.ListField()
    # 用户所在行业
    user_business = mongoengine.StringField(default='')
    # 受教育学校
    user_schools = mongoengine.ListField()
    # 专业
    user_majors = mongoengine.ListField()
    # 所在公司
    user_companies = mongoengine.ListField()
    # 所在公司职位
    user_jobs = mongoengine.ListField()
    # 个人简介
    user_description = mongoengine.StringField(default=0)
    # 获得赞同数 = 被收藏数+被感谢数
    user_vote_up_count = mongoengine.IntField(default=0)
    # 被收藏数
    user_favorite_count = mongoengine.IntField(default=0)
    # 被感谢数
    user_thanked_count = mongoengine.IntField(default=0)
    # 参与公共编辑数
    user_logs_count = mongoengine.IntField(default=0)
    # 关注数
    user_following = mongoengine.IntField(default=0)
    # 被关注数
    user_followers = mongoengine.IntField(default=0)
    # 参与赞助过的live 数
    user_participated_live_count = mongoengine.IntField(default=0)
    # 关注的话题数
    user_following_topic_count = mongoengine.IntField(default=0)
    # 关注的专栏数
    user_following_columns_count = mongoengine.IntField(default=0)
    # 关注的问题数
    user_following_question_count = mongoengine.IntField(default=0)
    # 关注的收藏夹
    user_following_favlists_count = mongoengine.IntField(default=0)
    # 回答数
    user_answer_count = mongoengine.IntField(default=0)
    # 分享数
    user_share_count = mongoengine.IntField(default=0)
    # 提问数
    user_question_count = mongoengine.IntField(default=0)
    # 收藏数
    user_collections = mongoengine.IntField(default=0)
    # 创建时间
    create_time = mongoengine.DateTimeField(default=datetime.now())
    # 徽章类型（type:best_answerer ;description:优秀回答者）还是其他
    badge_description = mongoengine.ListField()
    # 对应徽章（优秀回答）的话题
    badge_topics = mongoengine.ListField()


# 关注人的url
class FollowingUrl(mongoengine.Document):
    # 已经使用的url
    urlToken = mongoengine.StringField(default='')
    # 追踪队列里的url（异常或退出程序存入mongodb，方便下次继续爬取）
    queueUrl = mongoengine.StringField(default='none')


# 985 211 院校
class University985(mongoengine.Document):
    # 校名
    univ_name = mongoengine.StringField(default='')
    # 位置
    univ_place = mongoengine.StringField(default='')
    # 类型
    univ_type = mongoengine.StringField(default='')


# 211 院校
class University211(mongoengine.Document):
    # 校名
    univ_name = mongoengine.StringField(default='')
    univ_place = mongoengine.StringField(default='')
    # 位置
