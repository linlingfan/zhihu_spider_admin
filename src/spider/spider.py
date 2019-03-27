# __author_="gLinlf"
# coding=utf-8
import json
import threading

import requests
import time
from bs4 import BeautifulSoup

from src.spider import parse_save_info
from src.spider.globalvar import *
from src.spider.mongo import *
from src.spider import followingUrl
from src.proxy import getServiceIP
from src.logs.Logger import logger

MAX_TIME_OUT = 10
# 最大爬虫线程数
MAX_SPIDER_THREAD_NUM = 2


class ZhiHuUserSpider(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = 'running'

    def run(self):
        # 加载数据url
        LoadParam.load_url()
        spider_thread_list = []
        # 主爬虫优先启动
        # spider_thread = Spider()
        # spider_thread_list.append(spider_thread)
        # spider_thread.start()
        # print('main spider_thread is {0}'.format(spider_thread.status))
        # time.sleep(10)
        for s in range(MAX_SPIDER_THREAD_NUM):
            time.sleep(5)
            spider_thread = Spider()
            spider_thread_list.append(spider_thread)
            spider_thread.start()
            logger.info('spider_thread{0} is {1}'.format(s, spider_thread.status))
        # 监控爬虫状态 失败（403 或 爬取结束）结束（被屏蔽则关闭爬虫）
        while True:
            for Thread_spider in spider_thread_list:
                if Thread_spider.status == 'stop':
                    spider_thread_list.remove(Thread_spider)
                    logger.info('Thread_spider----{0} status is {1}'.format(Thread_spider, Thread_spider.status))
                    #     重新启动
                    spider_thread = Spider()
                    spider_thread_list.append(spider_thread)
                    spider_thread.start()
                else:
                    continue
            time.sleep(360)


class Spider(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = 'running'
        self.url = "https://www.zhihu.com/people/liaoxuefeng"
        self.session = requests.session()
        self.session.headers = header
        self.fetch_user_info = parse_save_info.ParseUserInfo()
        self.getProxyIp = getServiceIP.FetchProxyIP()
        self.getFollowingUrl = followingUrl.GetFollowingUrl()

    def run(self):
        try:
            self.get_user_html()
        except Exception as err:
            logger.debug('spider  get_user_html is err :{0}'.format(err))

    # 获取需要解析的用户个人中心网页
    def get_user_html(self):
        while self.url is not None:
            self.url = self.get_parse_url()
            following_url = self.url + "/following"
            logger.info('following_url is {0}'.format(following_url))
            try:
                while True:
                    # proxies_ip = get_proxies_ip()
                    proxies_ip = self.getProxyIp.get_proxies_ip()
                    if proxies_ip is not None:
                        logger.info("spider get proxies IP is: {0}".format(proxies_ip))
                        # get_html = requests.get(following_url, headers=header, verify=True,
                        #                         cookies=cookies2)
                        self.session.proxies = proxies_ip
                        # self.session.cookies = cookies2
                        get_html = self.session.get(following_url, timeout=MAX_TIME_OUT)
                        time.sleep(1)
                        break
                    else:
                        continue
                # get_html状态吗为200
                if get_html is not None and get_html.ok:
                    self.parse_html_info(get_html.text)
                # 如果状态码为403 forbidden n那么 说明账号被封程序先停止
                elif get_html.status_code == 403:
                    print(get_html.text)
                    logger.info('status_code is 403!!! forbidden progress return!')
                    return
                # 如果是其他 404问题 说明该账号用户账号被封或无效出现爬取异常，将数据库url修改成none
                elif get_html.status_code == 404 or get_html.status_code == 410:
                    logger.info("status_code is: {0} ! followingUrl:{1} is not invalid".format(get_html.status_code,
                                                                                             following_url))
                    self.change_queue_url2none(self.url)
                    continue
                else:
                    logger.info(
                        'get_html is:{0} or other and status_code is :{1}'.format(get_html.text, get_html.status_code))
                    continue
            except Exception as err:
                logger.debug('get_user_html{0} Exception is {1} '.format(following_url, err))
                continue
                # return
        else:
            logger.info("抓取结束！")
            return

    # 解析网页内容 获得用户数据
    def parse_html_info(self, source):
        try:
            soup = BeautifulSoup(source, "html5lib")
            # 分析页面 发现个人信息都在 id = "data" data-state={} 里面 获取源码，解析的到用户信息json串
            data_div = soup.find('div', attrs={'id': 'data'})
            if data_div is not None:
                data = soup.find('div', attrs={'id': 'data'}).attrs['data-state']
                # 将网页解析的用户信息转成json串data_json
                data_json = json.loads(str(data))
                # 首页中的所有用户集合
                all_users_data = data_json['entities']['users']
                if len(all_users_data) > 0 and all_users_data is not None:
                    # 截取用户连接中的名字
                    url_user_name = self.url.split("/")[-1]
                    user_data = all_users_data[url_user_name]
                    if len(user_data) > 0 and user_data is not None:
                        # 解析用户信息，存入数据库
                        self.fetch_user_info.parsed_user_info(user_data, self.url)
                        # 将已经解析获得用户信息的url值设为none
                        self.change_queue_url2none(self.url)
                        # 查询网页所有分页信息
                        pages_html = soup.find_all('button', attrs={'class': 'Button PaginationButton Button--plain'})
                        # 得到总页码数
                        if len(pages_html) > 0:
                            total_page = int(pages_html[-1].contents[0])
                        else:
                            total_page = 1
                        # 异步io爬取每一页的关注人地址(如果全局最大爬取页数为1页时候，直接爬取第一页following_url,减少page=1访问次数)
                        if max_page > 1:
                            self.getFollowingUrl.get_other_page_following(self.url, total_page)
                        else:
                            self.getFollowingUrl.add_following_url(all_users_data)
                    else:
                        logger.info('user_data is none!')
                else:
                    logger.info('all_users_data is none!')
            else:
                logger.info('data_div is none!(NoneType object has no attribute attrs)')
                self.change_queue_url2none(self.url)
        except Exception as err:
            logger.debug('parse_html_info err is : {0}'.format(err))
            self.change_queue_url2none(self.url)

    # 获得下一个要解析的url 如果为空从数据库拿取
    @staticmethod
    def get_parse_url():
        if not queue_follow_url.empty():
            using_url = queue_follow_url.get()
        else:
            # 从数据库加载已经爬取的url数据 和 之前在队列中的数据
            all_query_set = FollowingUrl.objects.all()
            for followingUrl in all_query_set:
                try:
                    # 加载所以已经爬取的url(再次判重，将重复的数据从数据库删除)
                    if followingUrl.urlToken not in had_url:
                        had_url.add(followingUrl.urlToken)
                        if followingUrl.queueUrl != 'none':
                            # 加载程序结束前队列中的url到队列中
                            queue_follow_url.put(followingUrl.queueUrl)
                        else:
                            continue
                    else:
                        logger.info("删除重复的 followingUrl:{0} 的 _id:{1}".format(followingUrl._data, followingUrl.id))
                        followingUrl.delete({'_id': str(followingUrl.id)})
                        continue
                except Exception as err:
                    logger.debug('get_parse_url err :{0}'.format(err))
                    logger.info('error happened in reload urls from mongodb!')
                    continue
            # 加载完毕 重新从队列取值
            if not queue_follow_url.empty() and len(had_url) > 0:
                using_url = queue_follow_url.get()
            elif queue_follow_url.empty() and len(had_url) == 0:
                # 爬虫入口
                using_url = follow_url_into
            else:
                logger.info("爬取结束了！")
                return
        return using_url

    # 将数据库中已经爬取解析的队列url值设为none（队列先进先出）
    @staticmethod
    def change_queue_url2none(used_url):
        # 将数据库中 （queueUrl） 已经出队列的url 为none
        # 返回所有符合查询条件的结果的文档对象列表
        query_set = FollowingUrl.objects(queueUrl=used_url)
        for updateFollowingUrl in query_set:
            try:
                updateFollowingUrl.queueUrl = 'none'
                updateFollowingUrl.save()
            except Exception as err:
                logger.debug('change_queue_url2none err :{0}'.format(err))
                continue


class LoadParam:
    def __init__(self):
        pass

    # 启动数据加载
    @staticmethod
    def load_url():
        logger.info("load url begin!")
        # 从数据库加载已经爬取的url数据 和 之前在队列中的数据
        all_query_set = FollowingUrl.objects.all()
        for followingUrl in all_query_set:
            try:
                # 加载所以已经爬取的url(再次判重，将重复的数据从数据库删除)
                if followingUrl.urlToken not in had_url:
                    had_url.add(followingUrl.urlToken)
                    if followingUrl.queueUrl != 'none':
                        # 加载程序结束前队列中的url到队列中
                        queue_follow_url.put(followingUrl.queueUrl)
                    else:
                        continue
                else:
                    logger.info("删除重复的 followingUrl:{0} 的 _id:{1}".format(followingUrl._data, followingUrl.id))
                    followingUrl.delete({'_id': str(followingUrl.id)})
                    continue
            except Exception as err:
                logger.debug('load url err :{0}'.format(err))
                logger.info('error happened in load urls from mongodb!')
                continue
        logger.info("load url end!")


if __name__ == '__main__':
    pass
    # object = ZhiHuUserSpider()
    # object.get_user_html()
