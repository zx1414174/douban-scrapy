import pymysql
from douban_scrapy.utils.tool.Builder import Builder
from douban_scrapy.settings import *


class MysqlTool:
    """
    数据库操作类
    """
    # 查询表名
    _table = ''
    # 表前缀
    _prefix_table = ''
    # 表主键名
    _primary_key = 'id'
    # 查询构造器
    __builder = None

    def __init__(self):
        con_data = MysqlTool.static_get_connect_data()
        self.__builder = Builder()
        self.__db = pymysql.connect(**con_data)
        self.__cursor = self.__db.cursor(pymysql.cursors.DictCursor)
        MysqlTool.static_language_handler(self.__db, self.__cursor)

    @staticmethod
    def static_get_connect_data():
        """
        获取连接配置信息
        :return:
        """
        con_data = dict()
        con_data['host'] = HOST
        con_data['user'] = USER
        con_data['password'] = PASSWORD
        con_data['port'] = PORT
        con_data['db'] = DB_NAME
        return con_data

    @staticmethod
    def static_language_handler(db, cursor):
        """
        数据库语言处理
        :param db:
        :param cursor:
        :return:
        """
        db.set_charset('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')

    def get_table_name(self):
        return self._prefix_table + self._table

    def insert(self, data):
        """
        插入数据
        :param dict data:插入数据
        :return:
        """
        table = self.get_table_name()
        keys = data.keys()
        key_string = ','.join(keys)
        # 拼接%s
        value_string = '%s,' * len(data)
        value_string = value_string[:-1]
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'\
            .format(table=table, keys=key_string, values=value_string)
        try:
            self.__cursor.execute(sql, tuple(data.values()))
            last_id = self.__cursor.lastrowid
            self.__db.commit()
            return last_id
        except Exception:
            self.__db.rollback()
            return False

    def count(self):
        """
        表数据数量
        :return:
        """
        table = self.get_table_name()
        sql = 'select count({primary_key}) as mysql_total from {table} {where}'\
            .format(primary_key=self._primary_key, table=table, where=self.__builder.build()).strip(' ')
        try:
            self.__cursor.execute(sql)
            row = self.__cursor.fetchone()
            return row['mysql_total']
        except:
            return False

    def find(self):
        """
        查找单条数据
        :return tuple:
        """
        table = self.get_table_name()
        sql = 'select * from {table} {where}'\
            .format(table=table, where=self.__builder.build()).strip(' ')
        try:
            self.__cursor.execute(sql)
            row = self.__cursor.fetchone()
            return row
        except:
            return False

    def get(self):
        """
        获取多条数据
        :return tuple:
        """
        sql = 'select * from {table} {where}'\
            .format(table=self.get_table_name(), where=self.__builder.build()).strip(' ')
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            return results
        except:
            return False

    def exit(self):
        """
        是否存在数据
        :return:
        """
        count = self.count()
        if count > 0:
            return True
        return False

    def search_sql(self, sql_str):
        """
        设置 查询sql
        :param sql_str:
        :return:
        """
        self.__builder.sql(sql_str)
        return self

    def set_table(self, table):
        """
        设置表名
        :param table:
        :return:
        """
        self._table = table
        return self

    def increase(self, primary_id, set_data):
        """
        增加字段数量
        :param int primary_id:主键id
        :param dict set_data:{字段名:增加的数量}
        :return:
        """
        table = self.get_table_name()
        sql = 'UPDATE {table} SET {set_sql} WHERE {primary_key} = %s'
        set_sql = ''
        param_data = []
        for field, num in set_data.items():
            set_sql += field + '=' + field + '+ %s' + ','
            param_data.append(num)
        set_sql = set_sql.strip(',')
        param_data.append(primary_id)
        sql = sql.format(table=table, set_sql=set_sql, primary_key=self._primary_key)
        # try:
        self.__cursor.execute(sql, tuple(param_data))
        self.__db.commit()
        return True
        # except:
        #     self.__db.rollback()
        #     return False

    def update(self, data):
        table = self.get_table_name()
        sql = 'UPDATE {table} SET {set_sql} {where}'
        set_sql = ''
        param_data = []
        for field, value in data.items():
            set_sql += field + '=' + '%s' + ','
            param_data.append(value)
        set_sql = set_sql.strip(',')
        sql = sql.format(table=table, set_sql=set_sql, where=self.__builder.build())
        try:
            self.__cursor.execute(sql, tuple(param_data))
            self.__db.commit()
            return True
        except:
            self.__db.rollback()
            return False











