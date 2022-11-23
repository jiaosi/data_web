
# 参考 https://www.jb51.net/article/190220.htm

import mysql.connector

class DB:
    __host="66.59.199.220" # 数据库主机地址
    __user="root"  # 数据库用户名
    __passwd="Mysql_147"  # 数据库密码
    __auth_plugin='mysql_native_password'

    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host = self.__host,
                user = self.__user,
                passwd = self.__passwd,
                auth_plugin = self.__auth_plugin
            )
        except Exception as e:
            print(e)
            exit()

        self.cursor = self.db.cursor()

    def close(self):
        try:
            self.cursor.close()
            self.db.close()
        except Exception as e:
            print(e)

    def get_record(self, sql, na):
        self.cursor.execute(sql, na)
        myresult = self.cursor.fetchall()  # fetchall() 获取所有记录
        return myresult

    def insert_record(self, sql, na):
        self.cursor.execute(sql, na)
        self.db.commit()

