from douban_scrapy.utils.mysql.MysqlTool import MysqlTool


class Error(MysqlTool):
    """
    错误信息表
    """
    _table = 'db_error'
