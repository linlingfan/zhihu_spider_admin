# __author_="gLinlf"
# coding=utf-8
import logging.config
# 日志类型（若配置为consoleLogger则输出到控制台，若配置为fileLogger则记录到日志文件中）
# LOGGER_TYPE = 'fileLogger'
LOGGER_TYPE = 'consoleLogger'
# 配置全局Logger
# 后台日志
configFile = open('E:\pyprojects\zhihu_admin\src\config\ZHAdminLogging.conf', encoding='utf8')
logging.config.fileConfig(configFile)
logger = logging.getLogger(LOGGER_TYPE)

# logger.info('4444')


