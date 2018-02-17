#!/usr/bin/env python
# coding=utf-8
"""
openwhois爬虫文件
"""
import requests
import re
from database import Table
from PIL import Image
import pytesseract
from io import BytesIO


class OpenSpider(object):
    """定义爬虫类"""

    def start(self, index):
        """
        爬虫启动入口
        :param index: 对应表的结尾序号
        """
        domains = Table(index).get_unexplored_domain()  # 获取需要爬取的域名
        re_link = re.compile('/data/whoishistory/\d')
        source = 'openwhois'
        for domain in domains:
            self.get_whowas(domain)

    def get_whowas_links(self, domain):
        """获取单个域名的whowas信息页面链接

        Args:
            domain (string): utf-8编码域名

        Returns:
            list: 指向各个whowas页面的相对url列表
        """
        r = requests.request('get', 'http://user.openwhois.com/data/history',
                             # todo: 将域名的中文部分转换成punycode编码
                             params={'DomainHistorySearch[domain]': domain},
                             allow_redirects=False)
        # 获取每条whowas的链接
        return re.findall('/data/whoishistory/\d+', r.text)

    def get_whowas(self, domain):
        """获取单个域名的所有whowas信息

        Args:
            domain (string): utf-8编码域名
        """
        links = self.get_whowas_links(domain)

        for link in links:
            # 获取每条whowas的具体信息
            result = requests.request(
                'get', 'http://openwhois.com{0}'.format(link)).text
            source = 'openwhois'
            domain_status = re.match(r'Domain Name: (\w+)', result)
            registrar = re.match(r'Registrar: ([\S ]+)', result)
            reg_name = re.match(r'Registrant Name: ([\S ]+)', result)
            reg_phone = re.match(r'Registrant Phone:([\S ]+)', result)
            # reg_email
            org_name = re.match(r'Registrant Organization: ([\S ]+)', result)
            name_server = re.match(r'Name Server: ([\S ]+)', result)
            creation_date = re.match(r'Creation Date: ([\S ]+)', result)
            expiration_date = re.match(
                r'Registry Expiry Date: ([\S ]+)', result)
            updated_date = re.match(r'Updated Date: ([\S ]+)', result)
#
# img_1 = requests.request('get' ,'http://email.openwhois.com/44c317e67c2d285720222e16541fdbc0.png')
# img_buffer = BytesIO(img_1.content)
# img = Image.open(img_buffer)
# print pytesseract.image_to_string(img)
# r = requests.request('get', 'http://user.openwhois.com/data/history',
#                      params={'DomainHistorySearch[domain]': 'baidu.com'},
#                      allow_redirects=False)
# # print r.text


r = requests.request('get', 'http://www.openwhois.com{0}'.format("/data/whoishistory/55764294"),
                     allow_redirects=False,
                     headers={'Host': 'www.openwhois.com',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'})

# print r.request.headers
# print r.content
print OpenSpider().get_whowas_links('中国.net')
