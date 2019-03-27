# __author_="gLinlf"
# coding=utf-8

from src.proxy import proxyIp
from src.spider import spider


class ZhiHuUser():
    def __init__(self):
        self.start_proxy_ip = proxyIp.ProxyIP()
        self.spiders = spider.ZhiHuUserSpider()

    def start(self):
        self.start_proxy_ip.start()
        # time.sleep(5)
        self.spiders.start()


if __name__ == '__main__':
    obj_start = ZhiHuUser()
    obj_start.start()
