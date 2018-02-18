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
import tldextract
# 指定系统默认编码为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


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
            self.get_whowas(self.domain_format(domain))

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
        links = self.get_whowas_links(self.domain_format(domain))

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
    
    def domain_format(self, raw_domain):
        """对含中文域名进行处理
        
        Args:
            raw_domain (string): 未处理域名
        
        Returns:
            string: punycode编码域名
        """
        extract = tldextract.extract(raw_domain)
        domain = extract[1]
        suffix = extract[2]
        domain = domain if domain.isalnum() else 'xn--' + unicode(domain).encode('punycode')
        suffix = suffix if suffix.isalnum() else 'xn--' + unicode(suffix).encode('punycode')
        return domain + '.' + suffix
#
# img_1 = requests.request('get' ,'http://email.openwhois.com/44c317e67c2d285720222e16541fdbc0.png')
# img_buffer = BytesIO(img_1.content)
# img = Image.open(img_buffer)
# print pytesseract.image_to_string(img)
# r = requests.request('get', 'http://user.openwhois.com/data/history',
#                      params={'DomainHistorySearch[domain]': 'baidu.com'},
#                      allow_redirects=False)
# # print r.text
