import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="123456"  # 数据库密码
)

def get_record(sql,na):

    mycursor = mydb.cursor()

    mycursor.execute(sql,na)

    myresult = mycursor.fetchall()  # fetchall() 获取所有记录

    return myresult
