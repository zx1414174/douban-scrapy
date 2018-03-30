from douban_scrapy.utils.mysql.MysqlTool import *


class Proxy(MysqlTool):
    # 定义表名
    _table = 'db_proxy'

    def get_rand_proxy(self):
        """
        获取一条随机代理数据
        :return:
        """
        search_sql = 'order by fail_num,rand() limit 1'
        result = self.search_sql(search_sql).find()
        if not result:
            return dict()
        return result

    def increase_fail_num(self, num=1):
        """
        新增fail_num
        :param num:
        :return:
        """




#
# proxy = Proxy()
# data = proxy.get_rand_proxy()
# print(data)
