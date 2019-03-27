# __author_="gLinlf"
# coding=utf-8
# 爬虫系统控制action
import os
import signal
from multiprocessing import Process, Queue

from decimal import Decimal

import time

from src import app
from src.spider.start import ZhiHuUser
from src.views.BaseView import *
from src.db.DBConnection import *
from src.logs.Logger import logger
# 由于Windows没有fork调用,使用multiprocessing模块跨平台版本的多进程模块。

# multiprocessing 队列用于多进程间的通信
pid_queue = Queue()


# 获得爬虫和数据状态
@app.route('/showStatus')
@allow_cross_domain
def show_spider_status():
    try:
        # 已经爬去的url
        all_url = db_f.find({}).count()
        # 已经解析的url
        had_parsed = db_f.find({'queueUrl': 'none'}).count()
        # 解析成功的url
        parsed_success = db.find({}).count()
        # 解析失败的url
        parsed_failure = had_parsed - parsed_success
        # 成功率
        rate = str(Decimal(str((parsed_success / had_parsed * 100))).quantize(Decimal('0.00')))
        # 总用户数
        all_users = parsed_success
        # 爬虫状态 1正在爬取 0结束爬取 查看爬虫进程是否存在
        if not pid_queue.empty():
            spider_status = 1
        else:
            spider_status = 0
            logger.info(
            "all_url:{0}, had_parsed:{1} ,parsed_success:{2} ,parsed_failure:{3} ,rate:{4}%,all_users:{5}".format(
                all_url, had_parsed, parsed_success, parsed_failure, rate, all_users))
        data_list = [{'all_url': all_url, 'had_parsed': had_parsed, 'parsed_success': parsed_success,
                      'parsed_failure': parsed_failure, 'rate': rate, 'all_users': all_users,
                      'spider_status': spider_status}]
        retn_dict = {'status': '000000', 'total': 1, 'pageSize': 10, 'curPage': 1, 'spiderStatus': spider_status,
                     'list': data_list}
        return jsonify(retn_dict)
    except:
        logger.info("获取爬虫状态信息失败！")
        error_dict = {'status': '999999'}
        return jsonify(error_dict)


# 未使用多线程出现 gevent.hub.LoopExit: This operation would block forever 错误 ？？？
# （spider里面使用了 协程（grequest ，基于gevent实现））
# 参考资料 https://github.com/gevent/gevent/issues/368
# gevent小结： http://blog.chinaunix.net/uid-9162199-id-4738168.html
# 打开爬虫进程
@app.route('/begin')
@allow_cross_domain
def begin_spider():
    print("start spider")
    status = '000000'
    if pid_queue.empty():
        try:
            logger.info('Parent process {0}'.format(os.getpid()))
            logger.info('spider_process is started now :')
            process = Process(target=spider_process, args=('spider_process', pid_queue,))
            process.start()
            # join()子进程结束后再继续往下运行，通常用于进程间的同步
            # process.join()
            time.sleep(3)
            if not pid_queue.empty():
                spider_status = 1
            else:
                spider_status = 0
        except:
            spider_status = 0
            status = '999999'
            logger.debug('进程启动异常！')
    else:
        spider_status = 1
        logger.info('进程已存在！正在爬取知乎信息！')
    retn_data = {'status': status, 'spiderStatus': spider_status}
    logger.info('返回状态:{0}和启动状态:{1}'.format(status, spider_status))
    return jsonify(retn_data)


# 关闭爬虫进程
@app.route('/close')
@allow_cross_domain
def close_spider():
    try:
        # 获得 进程共享 pid值
        if not pid_queue.empty():
            value = pid_queue.get()
            logger.info('kill pid'.format(value))
            os.kill(value, signal.SIGTERM)
        else:
            logger.info('进程不存在')
            # a = os.popen('taskkill.exe/pid:' + str(value)+'-t -f')
    except OSError:
        logger.info('没有如此进程!!!')
    logger.info('spider_process is closed！')

    return 'none'


# 调用爬虫系统的方法(多进程)
def spider_process(name, queue):
    logger.info('begin spider_process! ')
    logger.info('Run child process :{0} {1}..'.format(name, os.getpid()))
    pid = os.getpid()
    logger.info('subprocess pid is {0}'.format(pid))
    queue.put(pid)
    # 执行爬虫系统
    start_spider = ZhiHuUser()
    start_spider.start()
