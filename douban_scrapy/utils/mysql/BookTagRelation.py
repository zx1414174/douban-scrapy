from douban_scrapy.utils.mysql.MysqlTool import MysqlTool


class BookTagRelation(MysqlTool):
    _table = 'db_book_tag_relation'
