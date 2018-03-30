from douban_scrapy.utils.mysql.MysqlTool import MysqlTool


class Book(MysqlTool):
    """
    书籍
    """
    _table = 'db_book'
