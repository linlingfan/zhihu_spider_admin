# __author_="gLinlf"
# coding=utf-8
import logging.config
import queue
import redis
import configparser
from src.logs.Logger import logger
# from src.logs.SpiderLogger import logs


logger.info('1333'+'123')

t1 = [1,2]
t2=[]
# t2 = t1.copy()
t2=(t1).copy()
print(t2)
print(t1)
print(len({}))

section = 'redis_py'
CONFIG = configparser.ConfigParser()
CONFIG.read('redis-py.ini', encoding='utf8')
redis_host = CONFIG.get(section, "REDIS_HOST")
print(redis_host)
redis_port = CONFIG.get(section, "REDIS_PORT")
print(redis_port)
# redis_db = CONFIG.get(section, "REDIS_DB")
# 使用连接池
redis_pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=0)
rd = redis.Redis(connection_pool=redis_pool)

# print(rd.sadd("proxy_ip",3,2))

# print(rd.scard('proxy_ip'))

ls = [1, '2', {'12': 21}]
print({'12': 21} not in ls)

# s = set()
# s.add({'22': 33})
# print(s)

print('SDA'.lower())

for l in range(len(ls)):
    print(ls[l])

q = queue.Queue(10)

print(not q.empty())

# rd.set('for', 'bar')

# print(rd.get('for'))
