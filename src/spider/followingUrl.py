# __author_="gLinlf"
# coding=utf-8
import json

import grequests
from bs4 import BeautifulSoup

from src.proxy.proxyIp import *
from src.spider.globalvar import *
from src.spider.mongo import *
from src.proxy import getServiceIP
from src.logs.Logger import logger


class GetFollowingUrl:
    def __init__(self):
        self.getProxyIp = getServiceIP.FetchProxyIP()

    #  异步io爬取每一页的关注人url地址
    def get_other_page_following(self, url, total_pages):
        try:
            url_append_page = url + '/following?page='
            limit_page = max_page
            # 限制 因过多分页 花费在解析分页网页的时间（去掉(被关注)关注和被关注的关系 ，还存在 多人关注 同一个用户的情况,）
            # 上述关系可以在多数据中遍历到大部分拥有这个歌关系的用户信息，但是存在信息（只有关注关系的用户信息）不全面。
            # 传入的页码处理 一次传入5个 url
            if total_pages >= limit_page:
                total_pages = limit_page
            page_list = []
            for i in list(range(1, total_pages + 1)):
                page_list.append(url_append_page + (str(i)))
            # 页码数使5的倍数处理
            if total_pages % max_parse_page == 0:
                times = int(total_pages / max_parse_page)
            else:
                times = int(total_pages / max_parse_page) + 1
            # 截取链接数 5链接一个list
            page_cut_list = []
            for i in list(range(1, times + 1)):
                page_cut_list.append(page_list[max_parse_page * (i - 1): max_parse_page * i])
            print(page_cut_list)
            # 获取代理ip
            proxy_ip = self.getProxyIp.get_proxies_ip()
            # 循环 发送请求
            time.sleep(2)
            for url_list in page_cut_list:
                # 每次传多个url进去
                urls = url_list
                # rs = (grequests.get(u, headers=header, proxies=proxy_ip, cookies=cookies) for u in urls)
                rs = (grequests.get(u, headers=header, proxies=proxy_ip) for u in urls)
                respond_html = []
                for resp in grequests.map(rs, exception_handler=self.exception_handler):
                    # grequests.map查看异步io请求返回的状态码200 500
                    # print('status:{0} url:{1}'.format(resp, resp.url))
                    if resp is not None:
                        respond_html.append(resp.text)
                    else:
                        continue
                # 1。可以使用for循环一个一个解析，
                #  2.map/reduce 解析 一次领解析最多5个
                list(map(self.parse_page_html, respond_html))
        except Exception as err:
            logger.debug(" get_other_page_following error ！:{0}".format(err))

    # 解析每一页关注的用户信息
    def parse_page_html(self, page_html):
        try:
            soup_page = BeautifulSoup(page_html, 'html5lib')
            # 分析分页页面 得到个人信息，解析的到用户信息json串
            data = soup_page.find('div', attrs={'id': 'data'}).attrs['data-state']
            if data is not None:
                # 将网页解析的用户信息转成json串data_json
                data_json = json.loads(str(data))
                # 当前页所有user的数据集
                all_user_data = data_json['entities']['users']
                self.add_following_url(all_user_data)
            else:
                logger.info('parse_page_html data is none!')
        except Exception as err:
            logger.debug("parse_page_html error ! {0}".format(err))

    # 爬取该用户关注的其他用户的url set判重
    @staticmethod
    def add_following_url(follow_user__data):
        try:
            base_url = 'https://www.zhihu.com/people/'
            #  dict类型 keys 和values 可以使用如下遍历（也可以.keys()he .values()直接输出）
            for key, value in follow_user__data.items():
                new_url = base_url + (str(value['urlToken']))
                if new_url in had_url:
                    continue
                elif str(value['urlToken']) == 'None':
                    continue
                else:
                    # 存入had_url
                    had_url.add(new_url)
                    # 存入队列 had_url去重后队列值都是唯一性，未解析用户信息的url
                    logger.info('new following url is :{0}'.format(new_url))
                    queue_follow_url.put(new_url)
                    # 已经爬去的url和追踪队列中的url 存储到mongodb（已经去重）
                    db_url = FollowingUrl()
                    db_url.urlToken = new_url
                    db_url.queueUrl = new_url
                    db_url.save()
        except Exception as err:
            logger.debug('add_following_url has err :{0}'.format(err))

    # grequests异常处理
    @staticmethod
    def exception_handler(request, exception):
        logger.info('got exception request: {0}, exception {1}'.format(request, exception))
