class Builder:
    """
    数据库条件构造器
    """
    # 本表sql
    __self_sql = ''

    def sql(self, sql_str):
        """
        sql 输入sql查询
        :param str sql_str:
        :return:
        """
        self.__self_sql = sql_str

    def build(self):
        """
        返回sql字符串
        :return:
        """
        return self.__self_sql
