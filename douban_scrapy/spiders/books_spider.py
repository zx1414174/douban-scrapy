import scrapy
from douban_scrapy.utils.mysql.BookTag import BookTag
from douban_scrapy.settings import SPIDER_TAG_ID
from pyquery import PyQuery
from douban_scrapy.items.book_item import BookItem
from bs4 import BeautifulSoup
from douban_scrapy.utils.html.book_handler import BookHandler
import time


class BooksSpider(scrapy.Spider):
    name = "books_spider"

    __detail_info = {
        '作者:': 'author',
        '作者': 'author',
        '出版社:': 'publisher',
        '出版年:': 'publication_year',
        '页数:': 'pages',
        '定价:': 'price',
        '装帧:': 'layout',
        'ISBN:': 'isbn',
    }

    __headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Host': 'book.douban.com',
        'Referer': 'https://book.douban.com/'
    }

    def start_requests(self):
        """
        热门标签列表处理
        :return:
        """
        tag_id = SPIDER_TAG_ID
        book_tag_model = BookTag()
        tag = book_tag_model.search_sql('where id={tag_id}'.format(tag_id=tag_id)).find()
        url = tag['url']
        url = url.replace('tag//tag', 'tag').strip('/')
        start = 0
        while not False:
            start = start + 20
            param = '?start={start}&type=T'.format(start=start)
            page_url = url + param
            yield scrapy.Request(url=page_url, callback=self.parse_list, headers=self.__headers)

    def parse_list(self, response):
        """
        列表处理
        :param response:
        :return:
        """
        doc = PyQuery(response.text)
        detail_doc_list = doc('ul.subject-list > li > div.info > h2 a')
        for detail_item in detail_doc_list.items():
            detail_url = detail_item.attr('href')
            request = scrapy.Request(url=detail_url, callback=self.parse_book, headers=self.__headers)
            request.meta['url'] = detail_url
            yield request

    def parse_book(self, response):
        """
        书籍处理
        :param response:
        :return:
        """
        book_item = BookItem()
        soup = BeautifulSoup(response.text, 'lxml')
        div_doc = soup.select('#info span')
        for i, soup_item in enumerate(div_doc):
            if soup_item.string in self.__detail_info.keys():
                field_key = self.__detail_info[soup_item.string]
                book_item[field_key] = BookHandler.detail_info_handler(soup_item, field_key)
        book_item['url'] = response.meta['url'].strip('/')
        book_item['title'] = soup.select('#wrapper > h1 > span')[0].string
        book_item['subject_id'] = book_item['url'][book_item['url'].rfind('/')+1:]
        book_item['book_img'] = soup.select('#mainpic > a > img')[0].attrs['src']
        book_item['grade'] = soup.select('div.rating_self > strong.rating_num')[0].string.strip(' ')
        book_item['graded_number'] = soup.select('div.rating_sum > span > a > span')[0].string
        book_item['five_graded_percent'] = soup.select('div.rating_wrap > span.stars5')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_item['four_graded_percent'] = soup.select('div.rating_wrap > span.stars4')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_item['three_graded_percent'] = soup.select('div.rating_wrap > span.stars3')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_item['two_graded_percent'] = soup.select('div.rating_wrap > span.stars2')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_item['one_graded_percent'] = soup.select('div.rating_wrap > span.stars1')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        if len(soup.select('div.mod-hd > h2 > span.pl > a')) > 0:
            book_item['short_comment_count'] = soup.select('div.mod-hd > h2 > span.pl > a')[0].string.replace('全部', '').replace('条', '').strip(' ')
        else:
            book_item['short_comment_count'] = 0
        if len(soup.select('section.reviews > p.pl > a')) > 0:
            book_item['book_review_count'] = soup.select('section.reviews > p.pl > a')[0].string.replace('更多书评', '').replace('篇', '').replace('\n', '').replace(' ', '')
        else:
            book_item['book_review_count'] = 0
        if len(soup.select('div.ugc-mod > div.hd > h2 > span.pl > a > span')) > 0:
            book_item['note_count'] = soup.select('div.ugc-mod > div.hd > h2 > span.pl > a > span')[0].string
        else:
            book_item['note_count'] = 0
        now_time = int(time.time())
        book_item['create_time'] = now_time
        book_item['update_time'] = now_time
        return book_item



