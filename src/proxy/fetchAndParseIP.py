# __author_="gLinlf"
# coding=utf-8

# class RandomProxy: IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/ https:  http://www.xicidaili.com/wn/
# TODO 可重构 爬取多个免费代理网站
import requests
import time

from bs4 import BeautifulSoup
from src.proxy import validateIP
from src.logs.Logger import logger

header_ip = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
}

base_url = 'http://www.xicidaili.com/nn/'
# 最大爬取xici代理页码数
MAX_PROXY_PAGE = 5
# 连接超时timeout
MAX_TIME_OUT = 10
# 每次请求时间间隔
WAIT_REQUEST_TIME = 5


class ParseProxyIp:
    def __init__(self):
        self.session = requests.session()
        self.validate_IP = validateIP.ValidateProxyIP()

    # 获取代理网站的代理ip页面
    def get_proxy_ip_html(self, current_page):
        self.session.headers = header_ip
        # while current_page <= MAX_PROXY_PAGE:
        url = base_url + str(current_page)
        try:
            res = self.session.get(url, timeout=MAX_TIME_OUT)
            # 解析 获得 代理ip
            if res.status_code == 200 and res is not None:
                return res.text
                # all_ip_info = self.parse_proxy_ip(res.text)
                # # 校验ip可用性  和 去重
                # for i in range(len(all_ip_info)):
                #     if self.validate_IP.is_validate_ip(all_ip_info[i]):
                #         # 判断 该ip是否存在于 内存中有效代理ip
                #         # TODO 或使用 队列处理（存入全局的有效代理池中）
                #         validate_ip_list.append(all_ip_info[i])
                #     else:
            elif res.status_code == 403:
                logger.info('403 proxy ip web forbidden')
                return None
            else:
                logger.info('proxy ip web return code is :{0}'.format(res.status_code))
                return None
        except Exception as err:
            logger.info('ger_proxy_ip_html err:{0}, return status_code is {1}!'.format(err, res.status_code))
            return None

    # 解析 页面信息获得代理ip
    @staticmethod
    def parse_proxy_ip(web_data):
        if web_data is not None:
            try:
                soup = BeautifulSoup(web_data, 'html5lib')
                ips_tr = soup.find_all('tr')
                ip_info_list = []
                for i in range(1, len(ips_tr)):
                    ip_info = ips_tr[i]
                    tds = ip_info.find_all('td')
                    ip = str(tds[1].text)
                    port = str(tds[2].text)
                    protocol = str(tds[5].text).lower()
                    # 封装代理ip
                    ip_info = {'ip': ip, 'port': port, 'protocol': protocol}
                    ip_info_list.append(ip_info)
                logger.info('xicidaili get http ip proxy list is:{0}'.format(ip_info_list))
                return ip_info_list
            except Exception as err:
                logger.info('parse_proxy_ip err is :{0}'.format(err))
                return None
        else:
            logger.info('parse_proxy_ip fail web_data is None!')
            return None




            # 获得 https  代理
            # @staticmethod
            # def get_https_ip(web_data):
            #     soup = BeautifulSoup(web_data, 'html5lib')
            #     ips = soup.find_all('tr')
            #     ip_list = []
            #     for i in range(1, len(ips)):
            #         ip_info = ips[i]
            #         tds = ip_info.find_all('td')
            #         ip_list.append(tds[1].text + ':' + tds[2].text)
            #     print('xicidaili get https ip proxy list is', ip_list)
            #     return ip_list
