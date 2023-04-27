import time
import py2neo
import json
import datetime
import requests
import re
import random
from py2neo import Graph, Node, Relationship, NodeMatcher


# 获取系统时间函数
def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


class neo4j(object):
    graph = None
    date_now = ""

    def __init__(self):
        print("create neo4j class ...")
        # 连接数据库
        self.graph = Graph("http://180.76.165.98:7474", auth=("neo4j", "123456"))
        self.date_now = datetime.datetime.now().strftime("%Y%m%d")

    # 编写c1中间四个数字查询中国数据
    def get_c1_data(self):
        sql = "MATCH (n:`全球确诊数据`) where n.name='中国' and n.date='" + self.date_now + "' RETURN n"
        china_data = self.graph.run(sql).data()
        china_data = china_data[0]["n"]
        return china_data

    def get_c2_data(self):
        sql = "MATCH (n:`中国省份`) where n.date='" + self.date_now + "' RETURN n"
        province_data = self.graph.run(sql).data()
        return province_data

    def get_l1_data(self):
        sql = "MATCH (n:`全球确诊历史数据`) where n.name='中国' RETURN n"
        data_trend = self.graph.run(sql).data()
        return data_trend

    def get_l2_data(self):
        sql = "MATCH (n:`全球确诊历史数据`) where n.name='中国' RETURN n"
        data_trend = self.graph.run(sql).data()
        return data_trend

    def get_r1_data(self):
        # 新增省份显示
        sql = "MATCH (n:`每日国内新增前十`) where n.date='" + self.date_now + "' RETURN n"
        date_top = self.graph.run(sql).data()
        return date_top

    def get_r2_data(self):
        sql = "MATCH (n:`每日国内无症状新增前十`) where n.date='" + self.date_now + "' RETURN n"
        data_top = self.graph.run(sql).data()
        return data_top

    def get_world_map_data(self):
        world_sql = "MATCH (n:`国家`) where n.date='" + self.date_now + "' RETURN n"
        china_sql = "MATCH (n:`全球确诊数据`) where n.name='中国' and n.date='" + self.date_now + "' RETURN n"
        world_data = self.graph.run(world_sql).data()
        china_data = self.graph.run(china_sql).data()

        all_data = []
        china_data = china_data[0]["n"]
        for i in world_data:
            if i["n"]["country"] == "中国":
                continue
            all_data.append([i["n"]["country"], i["n"]["累计确诊"]])
        all_data.append(["中国", china_data["累计确诊"]])
        return all_data

    def get_world_data(self):
        sql = "MATCH (n:`全球确诊数据`) where n.date='" + self.date_now + "' RETURN n"
        all_data = self.graph.run(sql).data()
        confirm, suspect, heal, dead = 0, 0, 0, 0
        for i in all_data:
            value = i["n"]
            confirm += int(value["累计确诊"])
            suspect += int(value["新增确诊"])
            heal += int(value["累计治愈"])
            dead += int(value["累计死亡"])
        all_li = [confirm, suspect, heal, dead]
        return all_li

    def get_world_trend_data(self):
        sql = "MATCH (n:`全球确诊历史数据`) where n.name='全球' RETURN n"
        data_trend = self.graph.run(sql).data()
        return data_trend

    def get_world_global_data(self):
        sql = "MATCH (n:`六大洲确诊数据`) where n.date='" + self.date_now + "' RETURN n"
        data_global = self.graph.run(sql).data()
        return data_global

    def get_world_top_data(self):
        sql = "MATCH (n:`每日全球新增前十`) where n.date='" + self.date_now + "' RETURN n"
        add_data = self.graph.run(sql).data()
        return add_data

    def get_world_city_data(self):
        sql = "MATCH (n:`国外城市`) where n.date='" + self.date_now + "' RETURN n"
        city_data = self.graph.run(sql).data()
        num = random.randint(0, len(city_data) - 1)
        country = city_data[num]["n"]["f_node"]
        data_city = []
        for i in city_data:
            if i["n"]["f_node"] == country:
                data_city.append([i["n"]["city_name"], i["n"]["累计确诊"]])
        return country, data_city

    def get_china_city_data(self):
        sql = "MATCH (n:`中国城市`) where n.date='" + self.date_now + "' RETURN n"
        city_data = self.graph.run(sql).data()
        return city_data

    def get_search_data(self, country, city):
        if country == "中国":
            sql = "MATCH (n:`中国省份`) where n.province_name='" + city + "' and n.date='" + self.date_now + "' match (n)-[]->(m) RETURN m"
            china_data = self.graph.run(sql).data()
            return china_data
        else:
            sql = "MATCH (n:`国家`) where n.country='" + city + "' and n.date='" + self.date_now + "' match (n)-[]->(m) RETURN m"
            world_data = self.graph.run(sql).data()
            return world_data


# 测试
if __name__ == '__main__':
    country_data = neo4j().get_search_data("中国", "上海")
    country_list = []
    for i in country_data:
        country_list.append([i["m"]["city_name"], i["m"]["累计确诊"], i["m"]["累计治愈"], i["m"]["累计死亡"], i["m"]["新增确诊"]])
    print(country_list)