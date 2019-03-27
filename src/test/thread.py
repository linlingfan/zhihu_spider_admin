import queue
import threading

import time

from src.test import validate

PROXY_VALIDATE_THREAD_NUM = 2


class Thread1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # 初始化
        self.init()

        # 启动代理检验
        validate_thread_list = []
        # for i in range(PROXY_VALIDATE_THREAD_NUM):
        validate_thread = DoThread()
        validate_thread2 = DoThread2()
        validate_thread_list.append(validate_thread)
        validate_thread_list.append(validate_thread2)
        validate_thread.start()
        validate_thread2.start()

    print('end')

    @staticmethod
    def init():
        print('hello init!')


class DoThread2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = 'running'
        # 创建代理验证实例
        self.dataValidateModule = validate.testThd()

    def run(self):
        self.dataValidateModule.is_false()


class DoThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = 'running'
        # 创建代理验证实例
        self.dataValidateModule = validate.DataValidateModule()

    def run(self):
        try:
            self.dataValidateModule.is_real()
        except Exception as e:
            self.status = 'error'


            # 初始化，读取配置文件并配置


if __name__ == '__main__':
    obj = Thread1()
    obj.run()
