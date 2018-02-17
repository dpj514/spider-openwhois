# coding=utf-8

"""
数据库交互模块
"""

import MySQLdb


class Database(object):
    """定义数据库类"""
    def __init__(self):
        # todo: 后期添加配置文件
        self.db = MySQLdb.connect("***")


class Table(Database):
    """定义数据表类"""

    def __init__(self, index):
        """
        根据不同的表结尾序号生成不同实例
        :param index: 表结尾序号
        """
        Database.__init__(self)
        self.index = index

    def get_unexplored_domain(self):
        """获取数据库中whowas_flag为0的域名"""
        index = self.index
        sql_openwhois = 'SELECT domain FROM domain_{0} WHERE whowas_flag_openwhois = 0'.format(index)
        sql_cxw = 'SELECT domain FROM domain_{0} WHERE whowas_flag_cxw = 0'.format(index)
        sql_66whois = 'SELECT domain FROM domain_{0} WHERE whowas_flag_66whois = 0'.format(index)
        sql_table = {0: sql_openwhois, 1: sql_cxw, 2: sql_66whois}
        cursor = self.db.cursor()
        cursor.execute(sql_table[index])
        raw_data = cursor.fetchall()
        cursor.close()
        result = []
        for item in raw_data:
            result.append(item[0])
        return result

    def insert_whowas(self):
        """将获取的whowas插入表中"""
        sql = 'INSERT INTO whowas_{0} VALUES ({})'.format(self.index)