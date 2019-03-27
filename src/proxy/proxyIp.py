# 抓取免费代理线程（验证线程）
# 代理的使用
import queue
import threading

import time

from src.logs.Logger import logger
from src.proxy import fetchAndParseIP
from src.proxy import validateIP
from src.spider.globalvar import validate_proxy_pool

# 最大爬取xici代理页码数
MAX_PROXY_PAGE = 3
# 验证代理ip的线程数
VALIDATE_THREAD_NUM = 3
# 最小未检查的代理ip 队列（堆）先进先出
MIN_UNCHECKED_SIZE = 30
#
MAX_UNCHECKED_SIZE = 180
# 为检测的ip代理池
unchecked_ip_pool = queue.Queue(MAX_UNCHECKED_SIZE)
# 最小可用代理池
MIN_VALIDATE_POOL_SIZE = 8
# 旧的卡用代理池(用于可用代理的二次验证)
old_ip_pool = queue.Queue(50)


class ProxyIP(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = 'running'

    def run(self):
        # 线程池管理
        validate_thread_list = []
        # for i in range(PROXY_VALIDATE_THREAD_NUM):
        # 启动获取代理ip的线程
        fetch_parse_thread = FetchParseThread()
        fetch_parse_thread.start()
        logger.info('fetch and parse proxy ip thread is:{0}'.format(fetch_parse_thread.status))

        # 启动可用代理池扫描线程5 分钟扫描检测一次
        scan_proxy_thread = CheckValidateProxyPool()
        scan_proxy_thread.start()
        logger.info('scan validate proxy ip thread is:{0}'.format(scan_proxy_thread.status))

        # 启动代理ip验证线程(打开3个线程 加快验证)
        for i in range(VALIDATE_THREAD_NUM):
            validate_thread = ValidateIPThread()
            validate_thread_list.append(validate_thread)
            validate_thread.start()
            logger.info('validate_thread---- {0} status is {1}'.format(i, validate_thread.status))
        # 线程监控 如果发现线程出现异常 status= error 删除线程重新启动
        logger.info('unchecked_ip_pool size is :{0}'.format(unchecked_ip_pool.qsize()))
        logger.info('validate_proxy_pool size is :{0}'.format(validate_proxy_pool.qsize()))
        while True:
            if fetch_parse_thread.status == 'error':
                fetch_parse_thread = FetchParseThread()
                fetch_parse_thread.start()
                logger.info('获取代理IP线程出现问题，已经重新启动！')

            if scan_proxy_thread.status == 'error':
                scan_proxy_thread = CheckValidateProxyPool()
                scan_proxy_thread.start()
                logger.info('扫描检测可用代理线程出现问题，已经重新启动！')

            for thread in validate_thread_list:
                if thread.status == 'error':
                    validate_thread_list.remove(thread)
                    validate_thread = ValidateIPThread()
                    validate_thread_list.append(validate_thread)
                    logger.info('验证代理ip线程出现问题，已经重启！')
            time.sleep(300)


# 获取未检测代理
class FetchParseThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = 'running'
        self.fetch_parse_ip = fetchAndParseIP.ParseProxyIp()

    def run(self):
        while True:
            logger.info('FetchParseThread is running !')
            try:
                if validate_proxy_pool.qsize() < MIN_VALIDATE_POOL_SIZE and unchecked_ip_pool.qsize() < MIN_UNCHECKED_SIZE:
                    self.add_unchecked_to_queue()
                    time.sleep(180)
                else:
                    time.sleep(30)
            except Exception as err:
                logger.info('FetchParseThread err is :{0}'.format(err))
                self.status = 'error'

    def add_unchecked_to_queue(self):
        current_page = 1
        time.sleep(1)
        while current_page < MAX_PROXY_PAGE:
            ip_html = self.fetch_parse_ip.get_proxy_ip_html(current_page)
            ip_info_list = self.fetch_parse_ip.parse_proxy_ip(ip_html)
            current_page += 1
            for ip_info in ip_info_list:
                unchecked_ip_pool.put(ip_info)
                if unchecked_ip_pool.qsize() == MAX_UNCHECKED_SIZE:
                    break
                else:
                    continue

            if unchecked_ip_pool.qsize() == MAX_UNCHECKED_SIZE - VALIDATE_THREAD_NUM:
                break
            else:
                continue


class ValidateIPThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = 'running'
        self.validate_ip = validateIP.ValidateProxyIP()

    def run(self):
        try:
            self.add_validate_to_queue()
        except Exception as err:
            logger.info('ValidateIPThread err is:{0}'.format(err))
            self.status = 'error'

    # 新增可用代理到道理池
    def add_validate_to_queue(self):
        while True:
            if unchecked_ip_pool.qsize() > 0:
                unchecked_ip = unchecked_ip_pool.get()
                # print('unchecked_ip_pool.qsize', unchecked_ip_pool.qsize())
                # print('validate_proxy_pool.qsize', validate_proxy_pool.qsize())
                # print("is validate", self.validate_ip.is_validate_ip(unchecked_ip))
                if self.validate_ip.is_validate_ip(unchecked_ip):
                    validate_proxy_pool.put(unchecked_ip)
                else:
                    time.sleep(1)
            else:
                time.sleep(10)


# 隔5min时间检查可用代理ip池中的ip有有效性线程
class CheckValidateProxyPool(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = 'running'
        self.validate_ip = validateIP.ValidateProxyIP()

    def run(self):
        while True:
            logger.info('CheckValidateProxyPool is running !')
            try:
                self.get_old_ip()
                if not old_ip_pool.empty():
                    logger.info("begin scan validate ip ,old_ip_pool size is :{0}".format(old_ip_pool.qsize()))
                    for i in range(old_ip_pool.qsize()):
                        old_ip = old_ip_pool.get()
                        if self.validate_ip.is_validate_ip(old_ip):
                            # ip还有效则加入可用对列
                            validate_proxy_pool.put(old_ip)
                        else:
                            continue
                else:
                    logger.info('CheckValidateProxyPool is over!')
                # 五分检查一次
                time.sleep(240)
            except Exception as err:
                logger.info('CheckValidateProxyPool is err :{0}'.format(err))
                self.status = 'error'

    # 阿静对列中的可用ip加到旧ip对列
    # @staticmethod
    def get_old_ip(self):
        if not validate_proxy_pool.empty() and validate_proxy_pool.qsize() > 0:
            size = validate_proxy_pool.qsize()
            for i in range(size):
                if not validate_proxy_pool.empty():
                    old_ip_pool.put(validate_proxy_pool.get())
                else:
                    break
        else:
            time.sleep(1)


if __name__ == '__main__':
    obj = ProxyIP()
    obj.run()
