# __author_="gLinlf"
# coding=utf-8
import requests
import re

from src.logs.Logger import logger

headerr = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Cache-Control': 'no-cache',
    'Host': 'icanhazip.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
max_try_time = 1
max_time_out = 15
v_url = 'http://icanhazip.com/'


class ValidateProxyIP:
    def __init__(self):
        pass

    def is_validate_ip(self, ip_info):
        # def is_validate_ip(self):
        # if ip_info is None:
        #     return False
        # 截取ip值
        # ip_str = str(ip_info.get('http')).replace('http://', '')
        # real_ip = ip_str[0:ip_str.index(":")]
        # print('real_ip', real_ip)

        # 拼接ip
        ip = ip_info.get("ip")
        port = ip_info.get('port')
        protocol = ip_info.get('protocol')
        proxy_ip = {protocol: protocol + '://' + ip + ':' + port}
        logger.info('check proxy_ip :{0}'.format(proxy_ip))
        # proxy_ip = {'http': 'http//202.121.96.33:8086'}

        session = requests.session()
        session.headers = headerr
        session.proxies = proxy_ip
        retry_time = 0
        while retry_time < max_try_time:
            try:
                response = session.get(v_url, timeout=max_time_out)
                # print(response.status_code)
                # print(response.text)
                if response.status_code == 200:
                    match_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', response.text)
                    print(match_list)
                    if len(match_list) > 0:
                        current_ip = match_list.pop()
                        logger.info('current_ip:{0}'.format(current_ip))
                        if current_ip is not None and current_ip == ip:
                            logger.info('this is validate ip------------> {0}'.format(current_ip))
                            return True
                        else:
                            retry_time += 1
                            continue
                    else:
                        retry_time += 1
                        continue
            except Exception as err:
                logger.info('is_validate_ip err is :{0}'.format(err))
                return False
        return False


if __name__ == '__main__':
    obj = ValidateProxyIP()
    obj.is_validate_ip()
