# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from douban_scrapy.items.book_item import BookItem
from douban_scrapy.settings import SPIDER_TAG_ID
from douban_scrapy.utils.mysql.Book import Book
from douban_scrapy.utils.mysql.BookTagRelation import BookTagRelation


class DoubanScrapyPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            self.book_save_handler(item)

    def book_save_handler(self, book_item):
        """
        书籍信息保存处理
        :param book_item:
        :return:
        """
        book_mysql = Book()
        book_tag_relation_mysql = BookTagRelation()
        tag_id = SPIDER_TAG_ID
        book_where_sql = "where subject_id='{subject_id}'".format(subject_id=book_item['subject_id'])
        if not book_mysql.search_sql(book_where_sql).exit():
            book_id = book_mysql.insert(book_item)
            if not book_id:
                print(book_item['subject_id'] + '--error')
                raise Exception('书籍添加错误')
            else:
                print(book_item['subject_id'] + '--success')
        else:
            db_book_info = book_mysql.search_sql(book_where_sql).find()
            book_id = db_book_info['id']
        tag_where_sql = "where tag_id={tag_id} and book_id={book_id}".format(tag_id=tag_id, book_id=book_id)
        if not book_tag_relation_mysql.search_sql(tag_where_sql).exit():
            tag_relation = {
                'book_id': book_id,
                'tag_id': tag_id,
                'create_time': book_item['create_time'],
                'update_time': book_item['update_time'],
            }
            book_tag_relation_mysql.insert(tag_relation)
