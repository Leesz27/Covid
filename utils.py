import time
import pymysql


# 获取系统时间函数
def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


# 封装查询cov.sql数据库函数，导入数据库包
# (1)、定义封装连接
def get_cnn():
    """
    :return:
    """
    # 创建连接
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="root",
                           db="cov",
                           charset="utf8")
    # 封装游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


# (2)、关闭连接和游标
def close_conn(conn, cursor):
    cursor.close()
    conn.close()


# (3)、封装查询
def query(sql, *args):
    conn, cursor = get_cnn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


# 测试查询
def test():
    # 定义查询语句
    sql = "select * from details"
    # 调用通用封装查询
    res = query(sql)
    print(res)
    return res[0]  # res[0]


# 编写c1中间四个数字查询
def get_c1_data():
    sql = "SELECT confirm, suspect, heal, dead FROM `history` ORDER BY ds DESC LIMIT 1"
    res = query(sql)
    return res[0]


def get_c2_data():
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


def get_l1_data():
    sql = "SELECT ds, confirm, suspect, heal, dead FROM history ORDER BY ds ASC LIMIT 30;"
    res = query(sql)
    return res


def get_l2_data():
    sql = "select ds,confirm_add,suspect_add from history ORDER BY ds ASC LIMIT 30;"
    res = query(sql)
    return res


def get_r1_data():
    sql = 'select city,confirm from ' \
          '(select city,confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'order by confirm desc limit 5'
    res = query(sql)
    return res


def get_r2_data():
    sql = "SELECT ds, heal_add FROM history ORDER BY ds ASC LIMIT 30;"
    res = query(sql)
    return res


# 测试
if __name__ == '__main__':
    # print(get_time())
    # print(get_c1_data())
    # print(get_r2_data())
    data = get_r2_data()
    print(data)
    for i in data:
        print(i[0], i[1])

