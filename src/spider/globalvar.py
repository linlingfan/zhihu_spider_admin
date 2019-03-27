# __author_="gLinlf"
# coding=utf-8
import queue

# 定义全局变量

# 已经爬取得到所有url
had_url = set()
# 已经爬取解析用户的url
# had_used_url = set()
# 用户关注的其他用户的url 使用队列（使用后删除）
queue_follow_url = queue.Queue(maxsize=0)
# 爬虫入口
follow_url_into = 'https://www.zhihu.com/people/liaoxuefeng'
# 爬取代理IP地址
proxy_ip_url1 = 'http://www.xicidaili.com/nn/'
proxy_ip_url2 = 'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10'
proxy_https = 'http://www.xicidaili.com/wn/'
# 有效ip的代理池
validate_proxy_pool = queue.Queue(50)
# queue.LifoQueue LIFO 类似堆先进后厨 ；queue.Queue FIFO类似栈先进先出
# queue_follow_url.put('https://www.zhihu.com/people/competitionlaw')
# 请求头
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Cache-Control': 'no-cache',
    'host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
}
header1 = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
}
# 数据库名
db_name = 'zhihu_data'

# 抽样爬取不大于10个分页的用户(200人)（加快用户信息爬取速度！概率性减少 花费早爬取页面中存在较多已经爬去的用户url 的资源和时间。）
max_page = int(1)

# 异步IO请求解析的最大页码数
max_parse_page = int(1)

# # cookie要自己从浏览器获取
cookies = {}
cookies2 = {"d_c0": '"AGBCcCnS3AqPTrc9Iq8eTPWCQJWiGq0c860=|1479397734"',
            "_zap": "5dc4abdc-de17-4035-ba9e-1037bca34ff7",
            "_ga": "GA1.2.53592790.1481276979",
            "q_c1": "d37e0b8a213b484d903c29c8222ea06b|1489548790000|1489548790000",
            "nweb_qa": "heifetz",
            "r_cap_id": '"ZmEzNTI2ZWM1YjE5NDMyNWJkZGE1YTc3ODI4MjIyNWM=|1490792743|3952a3c68f2eff4c310beb678e6fdf12f8a2935b"',
            "cap_id": '"NGZjMDFkMmYxYzRlNDU2MWE5OGUwMDA2ZDBkYjhmZTI=|1490792743|3edeb3087ea873288cb5bb75b267cac9eac05fdc"',
            "l_cap_id": '"ZmY4YjgyY2U4OGUzNDgxNzg1MDcwMGJjZmZkMTM0NTY=|1490266538|d665ba315d54ecc6fc43d61814fd1c584e3ec8b7"',
            "capsion_ticket": '"2|1:0|10:1490266560|14:capsion_ticket|44:ZmUwMDA0N2I4ZTQ1NDhmYzgyZWJiZmE1MmMxNjgyYmY=|49763fdef78d014954606533a7a5609d37581e9add4e8f6ffaf43a5e02e633a3"',
            "_xsrf": "00d9e4688db76973b1f698d31f039836",
            "z_c0": "Mi4wQUFDQUhhTW9BQUFBWUVKd0tkTGNDaGNBQUFCaEFsVk54emI3V0FCNmlDSjFwV0Vwa1lweXIzZVNQTHhOekhqaFZB|1490425607|ed999a44e59dd8f8010ffc732485bdc1e6613946",
            "__utma": "51854390.53592790.1481276979.1490791536.1490792974.2",
            "__utmb": "51854390.0.10.1490425142",
            "__utmc": "51854390",
            "__utmz": "51854390.1490791536.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
            "__utmv": "51854390.100--|2=registration_date=20151220=1^3=entry_date=20151220=1"}
