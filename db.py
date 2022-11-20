import mysql.connector

mydb = mysql.connector.connect(
    host="66.59.199.220",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="Mysql_147",  # 数据库密码
    auth_plugin='mysql_native_password'
)

def get_record(sql,na):

    mycursor = mydb.cursor()

    mycursor.execute(sql,na)

    myresult = mycursor.fetchall()  # fetchall() 获取所有记录

    return myresult

def insert_record(sql, na):
    mycursor = mydb.cursor()
    mycursor.execute(sql, na)
    mydb.commit()