# __author_="gLinlf"
# coding=utf-8

import time

from src.logs.Logger import logger
from src.spider.globalvar import validate_proxy_pool

# 等待代理线程最大时间20
MAX_WAIT_PROXY_TIME = 30

# 最小ip数
MIN_PROXY_IP_POOL = 3


class FetchProxyIP:
    def __init__(self):
        self.get_proxies_ip()
        self.proxy_ip_info = None
        self.proxies_ip = {}

    # @staticmethod
    def get_proxies_ip(self):
        try:
            # 代理池是否有代理ip 且不少于四个，否则等待（代理线程爬取完毕）
            if not validate_proxy_pool.empty() and validate_proxy_pool.qsize() > MIN_PROXY_IP_POOL:
                self.proxy_ip_info = validate_proxy_pool.get()
                self.proxies_ip = {
                    self.proxy_ip_info.get('protocol'): 'http://' + self.proxy_ip_info.get(
                        'ip') + ':' + self.proxy_ip_info.get('port')}
                time.sleep(1)
                # 将代理ip返回队列
                validate_proxy_pool.put(self.proxy_ip_info)
            else:
                logger.info("等待代理ip线程获取代理或其他爬虫归还可用代理！")
                # 如果没有代理ip 使用本ip直接访问
                time.sleep(MAX_WAIT_PROXY_TIME)
                # validate_proxy_pool.put(123)
                self.proxies_ip = 1
                logger.info('使用本机ip或购买的稳定ip！proxies_ip = '.format(self.proxies_ip))
                # 如果代理ip量多稳定 ，使用递归调用，死等代理ip（该方法最稳）
                # self.get_proxies_ip()
                # TODO 不使用代理 (或者使用购买的稳定代理ip)
            return self.proxies_ip
        except Exception as err:
            logger.info('get_proxies_ip err is :{0}'.format(err))
            return None


            # @staticmethod
            # def get_random_validate_ip(ip_info_list):
            #     try:
            #         if ip_info_list is not None and len(ip_info_list) > 0:
            #             proxy_list = []
            #             for ip_info in ip_info_list:
            #                 proxy_list.append(
            #                     {ip_info.get('protocol'): 'http://' + ip_info.gey('ip') + ':' + ip_info.get('port')})
            #             proxy_ip = random.choice(proxy_list)
            #             return proxy_ip
            #         else:
            #             return None
            #     except Exception as err:
            #         print('get_random_validate_ip err is :', err)
            #         return None

            # 获得ip代理
            # TODO 代理ip需优化
            # def get_proxies_ip(self):
            #     try:
            #         # 代理池是否有代理ip 且不少于四个，否则等待（代理线程爬取完毕）
            #         if len(validate_ip_list) > 4 and self.get_random_validate_ip(validate_ip_list) is not None:
            #             proxy_ip = self.get_random_validate_ip(validate_ip_list)
            #         else:
            #             time.sleep(MAX_WAIT_PROXY_TIME)
            #             print("等待代理ip线程获取代理！")
            #             if len(validate_ip_list) > 4 and self.get_random_validate_ip(validate_ip_list) is not None:
            #                 proxy_ip = self.get_random_validate_ip(validate_ip_list)
            #             else:
            #                 # TODO 不使用代理 (或者使用购买的稳定代理ip)
            #                 proxy_ip = {'http': ''}
            #         print('内存代理ip:', validate_ip_list)
            #         return proxy_ip
            #     except Exception as err:
            #         print('get_proxies_ip err is :', err)
