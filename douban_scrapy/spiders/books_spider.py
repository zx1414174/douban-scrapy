import scrapy
from douban_scrapy.utils.mysql.BookTag import BookTag
from douban_scrapy.settings import SPIDER_TAG_ID


class BooksSpider(scrapy.Spider):
    name = "books"

    def start_requests(self):
        """
        热门标签列表处理
        :return:
        """
        tag_id = SPIDER_TAG_ID
        book_tag_model = BookTag()
        tag = book_tag_model.search_sql('where id={tag_id}'.format(tag_id=tag_id)).find()
        url = tag['url']
        url = url.strip('/')
        is_end = False
        start = 0
        while not is_end:
            start = start + 1
            param = '?start={start}&type=T'.format(start=start)
            page_url = url + param
            yield scrapy.Request(url=page_url, callback=self.parse_list)

    def parse_list(self, response):
        """
        列表处理
        :param response:
        :return:
        """
        pass

