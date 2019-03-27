# __author_="gLinlf"
# coding=utf-8
import time

from src.spider import mongo
from src.logs.Logger import logger


class ParseUserInfo:
    def __init__(self):
        # self.user_categories = mongo.UserInfoData()
        pass

    @staticmethod
    def parsed_user_info(user_data, user_url):
        #  user_info_categories 对象
        categories = mongo.UserInfoData()
        try:
            categories.user_url = user_url + "/following"
            logger.info('user_url:{0}'.format(categories.user_url))  # 用户姓名
            if 'name' in user_data.keys():
                categories.user_name = user_data['name'].strip()
                logger.info("user_name :{0}".format(categories.user_name))
            else:
                categories.user_name = ''
                logger.info("user_name is none ")
            # 用户头像地址
            if 'avatarUrl' in user_data.keys():
                categories.user_avatar_url = user_data['avatarUrl'].strip()
                logger.info('user_avatar_url:{0}'.format(categories.user_avatar_url))
            else:
                categories.user_avatar_url = ''
                logger.info('user_avatar_url is none')

            if 'headline' in user_data.keys():
                categories.user_head_line = user_data['headline'].strip()
                logger.info('user_head_line:{0}'.format(categories.user_head_line))
            else:
                categories.user_head_line = ''
                logger.info('user_head_line is none')
            # TODO 处理标题里面的连接
            # --------------------------获取性别gender  -1未知性别 0 女性 1男性 begin----------------------------
            if 'gender' in user_data.keys():
                gender = user_data['gender']
                if gender == 1:
                    categories.user_sex = 'man'
                elif gender == 0:
                    categories.user_sex = 'female'
                else:
                    categories.user_sex = 'none'
                logger.info("user_sex:{0}".format(categories.user_sex))
            else:
                categories.user_head_line = 'none'
                logger.info('user_sex is none')
            # ---------------------------获取性别gender  -1未知性别 0 女性 1男性 end----------------------------

            # -----------------------行业 begin----------------------------
            # 判断business key是否存在（不存在报异常）
            if 'business' in user_data.keys():
                data_business = user_data['business']
                if len(data_business) > 0 and data_business is not None:
                    categories.user_business = user_data['business']['name']
                    logger.info("user_business:{0}".format(categories.user_business))
                else:
                    categories.user_business = ''
                    logger.info("user_business is none")
            else:
                categories.user_business = ''
                logger.info("business key is none")
            # -----------------------行业 end----------------------------

            # ---------------------------用户居住所在地 begin---------------------------------------
            if 'locations' in user_data.keys():
                data_locations = user_data['locations']
                if len(data_locations) > 0 and data_locations is not None:
                    for i in range(len(data_locations)):
                        categories.user_locations.append(data_locations[i]['name'].strip())
                else:
                    logger.info('user_locations is none')
                logger.info('user_locations:{0}'.format(categories.user_locations))
            else:
                logger.info('user_locations is none')

            # ---------------------------用户居住所在地 end---------------------------------------

            #  --------------------------获取就读学校和专业 begin-------------------------
            if 'educations' in user_data.keys():
                data_educations = user_data['educations']
                if len(data_educations) > 0 and data_educations is not None:
                    for i in range(len(data_educations)):
                        if 'school' in data_educations[i].keys():
                            categories.user_schools.append(data_educations[i]['school']['name'].strip())
                        else:
                            categories.user_schools.append('none')
                        if 'major' in data_educations[i].keys():
                            categories.user_majors.append(data_educations[i]['major']['name'].strip())
                        else:
                            categories.user_majors.append('none')
                else:
                    logger.info('data_educations is none')
                logger.info("user_majors:{0}".format(categories.user_majors))
                logger.info("user_schools{0}".format(categories.user_schools))
            else:
                logger.info("data_educations is none")
            # --------------------------获取就读学校和专业 begin-------------------------
            # ---------------------------公司和公司职位 employments company  begin---------------------
            if 'employments' in user_data.keys():
                data_employments = user_data['employments']

                if len(data_employments) > 0 and data_employments is not None:
                    for i in range(len(data_employments)):
                        if 'company' in data_employments[i].keys():
                            categories.user_companies.append(data_employments[i]['company']['name'].strip())
                        else:
                            categories.user_companies.append('none')
                        if 'job' in data_employments[i].keys():
                            categories.user_jobs.append(data_employments[i]['job']['name'].strip())
                        else:
                            categories.user_jobs.append('none')
                else:
                    logger.info('data_employments is none')
                logger.info("user_companies:{0}".format(categories.user_companies))
                logger.info("user_jobs:{0}".format(categories.user_jobs))
            else:
                logger.info('data_employments is none')
            # ----------------------------公司和公司职位 employments company  end--------------------
            if 'description' in user_data.keys():
                categories.user_description = user_data['description'].strip()
                logger.info('user_description:{0}'.format(categories.user_description))
            else:
                categories.user_description = ''
                logger.info('user_description is none')
            # TODO 字符串里面标签处理
            # 被赞同数
            if 'voteupCount' in user_data.keys():
                categories.user_vote_up_count = user_data['voteupCount']
                logger.info('user_vote_up_count:{0}'.format(categories.user_vote_up_count))
            else:
                categories.user_vote_up_count = 0
                logger.info('user_vote_up_count is none')
            # 被收藏数
            if 'favoritedCount' in user_data.keys():
                categories.user_favorite_count = user_data['favoritedCount']
                logger.info('user_favorite_count:{0}'.format(categories.user_favorite_count))
            else:
                categories.user_favorite_count = 0
                logger.info('user_favorite_count is none')
            # 被感谢数
            if 'thankedCount' in user_data.keys():
                categories.user_thanked_count = user_data['thankedCount']
                logger.info('user_thanked_count:{0}'.format(categories.user_thanked_count))
            else:
                categories.user_thanked_count = 0
                logger.info('user_thanked_count is none')
            # 参与公共编辑数
            if 'logsCount' in user_data.keys():
                categories.user_logs_count = user_data['logsCount']
                logger.info('user_logs_count:{0}'.format(categories.user_logs_count))
            else:
                categories.user_logs_count = 0
                logger.info('user_logs_count is none')
            # 关注数
            if 'followingCount' in user_data.keys():
                categories.user_following = user_data['followingCount']
                logger.info('user_following:{0}'.format(categories.user_following))
            else:
                categories.user_following = 0
                logger.info('user_following is none')
            # 被关注数
            if 'followerCount' in user_data.keys():
                categories.user_followers = user_data['followerCount']
                logger.info('user_followers:{0}'.format(categories.user_followers))
            else:
                categories.user_followers = 0
                logger.info('user_followers is none')
            # 参与赞助过的live 数
            if 'participatedLiveCount' in user_data.keys():
                categories.user_participated_live_count = user_data['participatedLiveCount']
                logger.info('user_participated_live_count:{0}'.format(categories.user_participated_live_count))
            else:
                categories.user_participated_live_count = 0
                logger.info('user_participated_live_count is none')
            # 关注的话题数
            if 'followingTopicCount' in user_data.keys():
                categories.user_following_topic_count = user_data['followingTopicCount']
                logger.info('user_following_topic_count:{0}'.format(categories.user_following_topic_count))
            else:
                categories.user_following_topic_count = 0
                logger.info('user_following_topic_count is none')
            # 关注的专栏数
            if 'followingColumnsCount' in user_data.keys():
                categories.user_following_columns_count = user_data['followingColumnsCount']
                logger.info('user_following_columns_count:{0}'.format(categories.user_following_columns_count))
            else:
                categories.user_following_columns_count = 0
                logger.info('user_following_columns_count is none')
            # 关注的问题数
            if 'followingQuestionCount' in user_data.keys():
                categories.user_following_question_count = user_data['followingQuestionCount']
                logger.info('user_following_question_count:{0}'.format(categories.user_following_question_count))
            else:
                categories.user_following_question_count = 0
                logger.info('user_following_question_count is none')
            # 关注的收藏夹
            if 'followingFavlistsCount' in user_data.keys():
                categories.user_following_favlists_count = user_data['followingFavlistsCount']
                logger.info('user_following_favlists_count:{0}'.format(categories.user_following_favlists_count))
            else:
                categories.user_following_favlists_count = 0
                logger.info('user_following_favlists_count is none')
            # 回答数
            if 'answerCount' in user_data.keys():
                categories.user_answer_count = user_data['answerCount']
                logger.info('user_answer_count:{0}'.format(categories.user_answer_count))
            else:
                categories.user_answer_count = 0
                logger.info('user_answer_count is none')
            # 分享数
            if 'articlesCount' in user_data.keys():
                categories.user_share_count = user_data['articlesCount']
                logger.info('user_share_count:{0}'.format(categories.user_share_count))
            else:
                categories.user_share_count = 0
                logger.info('user_share_count is none')
            # 提问数
            if 'questionCount' in user_data.keys():
                categories.user_question_count = user_data['questionCount']
                logger.info('user_question_count:{0}'.format(categories.user_question_count))
            else:
                categories.user_question_count = 0
                logger.info('user_question_count is none')
            # 收藏数
            if 'favoriteCount' in user_data.keys():
                categories.user_collections = user_data['favoriteCount']
                logger.info('user_collections:{0}'.format(categories.user_collections))
            else:
                categories.user_collections = 0
                logger.info('user_collections is none')
            # 勋章类型（是否是最好回答者） 勋章话题（回答的相关话题）
            if 'badge' in user_data.keys():
                badge_data = user_data['badge']
                if len(badge_data) > 0:
                    for i in range(len(badge_data)):
                        categories.badge_description.append(badge_data[i]['description'])
                        if len(badge_data[i]['topics']) > 0:
                            for m in range(len(badge_data[i]['topics'])):
                                categories.badge_topics.append(badge_data[i]['topics'][m]['name'])
                        else:
                            categories.badge_topics = []
                    logger.info('badge_description:{0}, badge_topics:{1}'.format(
                        categories.badge_description, categories.badge_topics))
                else:
                    categories.badge_description = []
                    categories.badge_topics = []
                    logger.info('badge description and topics is none')
            else:
                logger.info('badge is none')
            logger.info('--------------------------------------------------------------------')

        except Exception as err:
            logger.info('Exception is :{0}'.format(err))
            logger.info("parsed user info err or ser_data is none!")
        try:
            time.sleep(1)
            categories.save()
        except Exception as err:
            logger.info('save to db err is:{0}'.format(err))
            logger.info('mongodb data save fail!!! url is {0}'.format(categories.user_url))
