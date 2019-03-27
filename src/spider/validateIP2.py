# __author_="gLinlf"
# coding=utf-8
import requests
import re

headerr = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Cache-Control': 'no-cache',
    'Host': 'icanhazip.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
max_try_time = 2
max_time_out = 15
v_url = 'http://icanhazip.com/'


class ValidateProxyIP2:
    def __init__(self):
        self.session = requests.session()

    def is_validate_ip(self, ip_info):
        # def is_validate_ip(self):
        # ip_info = {'http': 'http//175.155.24.4:808'}
        if ip_info is None:
            return False
        # 截取ip值
        ip_str = str(ip_info.get('http')).replace('http://', '')
        real_ip = ip_str[0:ip_str.index(":")]

        print('real_ip', real_ip)
        self.session = requests.session()
        self.session.headers = headerr
        self.session.proxies = ip_info
        print(self.session.proxies)
        retry_time = 0
        while retry_time < max_try_time:
            try:
                response = self.session.get(v_url, timeout=max_time_out)
                print(response.text)
                if response.status_code == 200:
                    match_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', response.text)
                    print(match_list)
                    if len(match_list) > 0:
                        current_ip = match_list.pop()
                        print('current_ip', current_ip)
                        if current_ip is not None and current_ip == real_ip:
                            print('True')
                            return True
                        else:
                            retry_time += 1
                    else:
                        retry_time += 1
            except Exception as err:
                print(err)
                retry_time += 1
        return False


if __name__ == '__main__':
    obj = ValidateProxyIP2()
    obj.is_validate_ip()
