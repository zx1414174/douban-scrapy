class BookHandler:
    """
    豆瓣读书处理类
    """
    @staticmethod
    def detail_info_handler(soup_item, field_key):
        """
        书籍详情信息模块处理
        :param soup_item:
        :return str:
        """
        method = 'static_detail_info_{param}_handler'
        method = method.format(param=field_key)
        return getattr(BookHandler, method)(soup_item)

    @staticmethod
    def static_detail_info_author_handler(soup_item):
        """
        处理书籍作者信息
        :param soup_item:
        :return str:
        """
        return soup_item.next_sibling.next_sibling.string.replace(' ', '').replace('\n', '')

    @staticmethod
    def static_detail_info_publisher_handler(soup_item):
        """
        书籍出版社信息
        :return str:
        """
        return BookHandler.static_detail_info_normal_handler(soup_item)

    @staticmethod
    def static_detail_info_publication_year_handler(soup_item):
        """
        书籍出版年份信息
        :param soup_item:
        :return str:
        """
        return BookHandler.static_detail_info_normal_handler(soup_item)

    @staticmethod
    def static_detail_info_pages_handler(soup_item):
        """
        书籍页数信息
        :param soup_item:
        :return str:
        """
        return BookHandler.static_detail_info_normal_handler(soup_item).replace('页', '').strip(' ')

    @staticmethod
    def static_detail_info_price_handler(soup_item):
        """
        书籍价格信息
        :param soup_item:
        :return str:
        """
        return soup_item.next_sibling.\
            replace('元', '').replace('CNY', '').replace('HK$', '').replace('NTD', '').\
            replace('（全两册）', '').replace('（全三册）', '').strip(' ')

    @staticmethod
    def static_detail_info_isbn_handler(soup_item):
        """
        书籍isbn信息
        :param soup_item:
        :return str:
        """
        return BookHandler.static_detail_info_normal_handler(soup_item)

    @staticmethod
    def static_detail_info_layout_handler(soup_item):
        """
        书籍装帧信息
        :param soup_item:
        :return str:
        """
        return BookHandler.static_detail_info_normal_handler(soup_item)

    @staticmethod
    def static_detail_info_normal_handler(soup_item):
        """
        书籍信息通用处理方案
        :param soup_item:
        :return str:
        """
        return soup_item.next_sibling.strip(' ')
