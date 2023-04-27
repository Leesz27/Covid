import sys
import time
import json
import datetime
import requests
import re
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo

"""
caseList    中国疫情（目前） **
caseOutsideList 国外疫情（目前） **
hotwords    热搜 *
summaryDataIn   中国确诊数据 *
summaryDataOut  国外确诊数据 *
trend   中国历史数据   **
globalList  七大洲疫情数据  **
allForeignTrend 全球历史数据  **
topAddCountry   每日全球新增前十  **
topOverseasInput    累计国内境外输入新增前十
asymptomaticTopProvince 每日国内无症状新增前十
newAddTopProvince   每日国内新增前十数量
topCountryAddTrend  顶部国家新增趋势（17个）历史数据
"""


class Epidemic_crawling(object):
    # 疫情爬取
    jsonAll = ""
    graph = None
    day_now = ""

    def __init__(self):
        print("create Epidemic class ...")

        # url链接
        url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner'
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'\
                    '80.0.3987.122 Safari/537.36"
        }
        response = requests.get(url=url, headers=headers)
        data = response.text

        all_json = re.findall('"component":\[(.*)\],', data)[0]
        self.jsonAll = json.loads(all_json)

        self.day_now = datetime.datetime.now().strftime("%Y%m%d")

        # 连接数据库
        # self.graph = Graph("http://106.13.216.149:7474", user="neo4j", password="123456")
        self.graph = Graph("http://180.76.165.98:7474", user="neo4j", password="123456")

        time_now = self.graph.run("match (n:time) return n").data()
        if not time_now:
            self.graph.run("create (n:time {date:'" + self.day_now + "'})")
            try:
                self.graph.run("create constraint on (n:time) assert n.date is unique")
            except:
                pass
        else:
            try:
                self.graph.run("create (n:time {date:'" + self.day_now + "'})")
            except Exception as e:
                pass

    def get_china_data(self):

        # 获取每日国内疫情数据,caseList    中国疫情（目前）
        china_data_json = self.jsonAll["caseList"]

        time_date = self.graph.run(
            "match (n:`国家`) where n.country='中国' and n.date='" + self.day_now + "' return n").data()
        if time_date:
            pass
        else:
            self.graph.run("create (n:`国家` {country:'中国', date:'" + self.day_now + "'})")
            self.graph.run(
                "match (n:time),(m:`国家`) where n.date='" + self.day_now + "' and m.country='中国' and m.date='" +
                self.day_now + "' create (n)-[:relation {country:'中国', date:'" + self.day_now + "'}]->(m)")

            for i in china_data_json:
                neo4j_province_name = "中国省份"
                # 创建节点
                province_node = Node(neo4j_province_name, province_name=i["area"])
                province_node["累计确诊"] = i["confirmed"]
                province_node["累计死亡"] = i["died"]
                province_node["累计治愈"] = i["crued"]
                province_node["新增确诊"] = i['confirmedRelative']
                province_node["新增死亡"] = i['diedRelative']
                province_node["新增治愈"] = i['curedRelative']
                province_node["新增无症状感染者"] = i['asymptomaticRelative']
                province_node["无症状感染者"] = i['asymptomatic']
                province_node["本土新增"] = i['nativeRelative']
                province_node["现有确诊"] = i['curConfirm']
                province_node["新增确诊"] = i['curConfirmRelative']
                province_node["未新增日期"] = i['noNativeRelativeDays']
                province_node["境外输入"] = i['overseasInputRelative']
                province_node["date"] = str(self.day_now)
                # 创建节点
                self.graph.create(province_node)

                # 连接省份与国家
                self.graph.run(
                    "match (n:`国家`),(m:`中国省份`) where n.country='中国' and n.date='" + self.day_now + "' and m.province_name='" +
                    i["area"] + "' and m.date='" + self.day_now + "' create (n)-[:relation {province:'" + i[
                        "area"] + "', date:'" + self.day_now + "'}]->(m)")

                if i['subList']:
                    neo4j_city_name = "中国城市"
                    for j in i['subList']:
                        city_node = Node(neo4j_city_name, city_name=j["city"])
                        city_node["累计确诊"] = j["confirmed"]
                        city_node["累计死亡"] = j["died"]
                        city_node["累计治愈"] = j["crued"]
                        city_node["新增确诊"] = j["confirmedRelative"]
                        city_node["新增无症状感染者"] = j["asymptomaticRelative"]
                        city_node["无症状感染者"] = j["asymptomatic"]
                        city_node["本土新增"] = j["nativeRelative"]
                        city_node["现有确诊"] = j["curConfirm"]
                        city_node["未新增日期"] = j["noNativeRelativeDays"]
                        city_node["date"] = str(self.day_now)
                        city_node["f_node"] = i["area"]
                        # 创建节点
                        self.graph.create(city_node)
                        self.graph.run(
                            "match (n:`中国省份`),(m:`中国城市`) where n.province_name='" + i[
                                "area"] + "' and n.date='" + self.day_now + "' and m.city_name='" + j[
                                "city"] + "' and m.date='" + self.day_now + "' and m.f_node='" + i[
                                "area"] + "' create (n)-[:relation {city:'" + i[
                                "area"] + "', date:'" + self.day_now + "'}]->(m)")

        print("中国每日疫情数据更新完毕!")

    def get_world_data(self):

        # 获取每日国外疫情数据    caseOutsideList 国外疫情（目前）
        world_data_json = self.jsonAll["caseOutsideList"]
        for i in world_data_json:
            time_date = self.graph.run(
                "match (n:`国家`) where n.country='" + i["area"] + "' and n.date='" + self.day_now + "' return n").data()
            if time_date:
                continue
            else:
                neo4j_country_name = "国家"

                country_node = Node(neo4j_country_name, country=i["area"])
                country_node["累计确诊"] = i["confirmed"]
                country_node["累计死亡"] = i["died"]
                country_node["累计治愈"] = i["crued"]
                country_node["新增确诊"] = i['confirmedRelative']
                country_node["新增死亡"] = i['diedRelative']
                country_node["新增治愈"] = i['curedRelative']
                country_node["现有确诊"] = i['curConfirm']
                country_node["新增确诊"] = i['curConfirmRelative']
                country_node["治愈率"] = i["curedPercent"]
                country_node["死亡率"] = i["diedPercent"]
                country_node["date"] = str(self.day_now)
                # 创建节点
                self.graph.create(country_node)
                self.graph.run(
                    "match (n:time),(m:`国家`) where n.date='" + self.day_now + "' and m.country='" + i[
                        "area"] + "' and m.date='" + self.day_now + "' create (n)-[:relation {country:'" + i[
                        "area"] + "', date:'" + self.day_now + "'}]->(m)")

                if i['subList']:
                    neo4j_city_name = "国外城市"
                    for j in i['subList']:
                        city_node = Node(neo4j_city_name, city_name=j["city"])
                        city_node["累计确诊"] = j["confirmed"]
                        city_node["累计死亡"] = j["died"]
                        city_node["累计治愈"] = j["crued"]
                        city_node["新增确诊"] = j["confirmedRelative"]
                        city_node["新增死亡"] = j["diedRelative"]
                        city_node["现有确诊"] = j["curConfirm"]
                        city_node["治愈率"] = j["curedPercent"]
                        city_node["死亡率"] = j["diedPercent"]
                        city_node["date"] = str(self.day_now)
                        city_node["f_node"] = i["area"]
                        # 创建节点
                        self.graph.create(city_node)
                        self.graph.run(
                            "match (n:`国家`),(m:`国外城市`) where n.country='" + i[
                                "area"] + "' and n.date='" + self.day_now + "' and m.city_name='" + j[
                                "city"] + "' and m.date='" + self.day_now + "' and m.f_node='" + i[
                                "area"] + "' create (n)-[:relation {city:'" + i[
                                "area"] + "', date:'" + self.day_now + "'}]->(m)")
        print("全球每日疫情数据更新完毕!")

    def get_hot_words(self):
        # hotwords    热搜
        hot_words_json = self.jsonAll["hotwords"]
        neo4j_hot_name = "hot"
        hot = self.graph.run("match (n:hot) where n.date='" + self.day_now + "' return n").data()
        if hot:
            pass
        else:
            for i in hot_words_json:
                hot_node = Node(neo4j_hot_name, query=i["query"])
                hot_node["热度"] = i["degree"]
                hot_node["date"] = str(self.day_now)
                self.graph.create(hot_node)
        print("每日疫情热搜数据更新完毕!")

    def get_china_sumdata(self):
        # summaryDataIn 中国确诊数据
        china_sum_json = self.jsonAll["summaryDataIn"]
        neo4j_sum_name = "全球确诊数据"
        time_date = self.graph.run(
            "match (n:`全球确诊数据`) where n.name='中国' and n.date='" + self.day_now + "' return n").data()
        if time_date:
            pass
        else:
            china_sumdate = Node(neo4j_sum_name, name="中国")
            china_sumdate["累计确诊"] = china_sum_json["confirmed"]
            china_sumdate["累计死亡"] = china_sum_json["died"]
            china_sumdate["累计治愈"] = china_sum_json["cured"]
            china_sumdate["累计境外"] = china_sum_json["overseasInput"]
            china_sumdate["新增确诊"] = china_sum_json["confirmedRelative"]
            china_sumdate["新增本土"] = china_sum_json["unOverseasInputNewAdd"]
            china_sumdate["新增境外"] = china_sum_json["overseasInputRelative"]
            china_sumdate["新增无症状"] = china_sum_json["asymptomaticRelative"]
            china_sumdate["现有确诊"] = china_sum_json["curConfirm"]
            china_sumdate["现有本土"] = china_sum_json["curLocalConfirm"]
            china_sumdate["现有境外"] = china_sum_json["curOverseasInput"]
            china_sumdate["date"] = str(self.day_now)
            self.graph.create(china_sumdate)
        print("中国疫情数据更新完毕!")

    def get_world_sumdata(self):
        # summaryDataOut  国外确诊数据
        world_sumdata_json = self.jsonAll["summaryDataOut"]
        neo4j_sum_name = "全球确诊数据"
        time_date = self.graph.run(
            "match (n:`全球确诊数据`) where n.name='全球' and n.date='" + self.day_now + "' return n").data()
        if time_date:
            pass
        else:
            world_sum_date = Node(neo4j_sum_name, name="全球")
            world_sum_date["累计确诊"] = world_sumdata_json["confirmed"]
            world_sum_date["累计死亡"] = world_sumdata_json["died"]
            world_sum_date["累计治愈"] = world_sumdata_json["cured"]
            world_sum_date["新增确诊"] = world_sumdata_json["confirmedRelative"]
            world_sum_date["新增治愈"] = world_sumdata_json["curedRelative"]
            world_sum_date["新增死亡"] = world_sumdata_json["diedRelative"]
            world_sum_date["治愈率"] = world_sumdata_json["curedPercent"]
            world_sum_date["死亡率"] = world_sumdata_json["diedPercent"]
            world_sum_date["date"] = str(self.day_now)
            self.graph.create(world_sum_date)
        print("全球疫情数据更新完毕!")

    def get_china_trend(self):
        # trend   中国近三个月历史数据
        china_trend_json = self.jsonAll["trend"]
        year = datetime.datetime.now().strftime("%Y")
        neo4j_history_name = "全球确诊历史数据"

        for i in range(len(china_trend_json["updateDate"])):
            month, day = china_trend_json["updateDate"][i].split(".")
            date = year + month + day
            time_date = self.graph.run(
                "match (n:`全球确诊历史数据`) where n.name='中国' and n.date='" + date + "' return n").data()
            if time_date:
                continue
            else:
                china_trend_data = Node(neo4j_history_name, name='中国')
                china_trend_data["确诊"] = china_trend_json["list"][0]["data"][i]
                china_trend_data["疑似"] = china_trend_json["list"][1]["data"][i]
                china_trend_data["治愈"] = china_trend_json["list"][2]["data"][i]
                china_trend_data["死亡"] = china_trend_json["list"][3]["data"][i]
                china_trend_data["新增确诊"] = china_trend_json["list"][4]["data"][i]
                china_trend_data["新增疑似"] = china_trend_json["list"][5]["data"][i]
                china_trend_data["新增治愈"] = china_trend_json["list"][6]["data"][i]
                china_trend_data["新增死亡"] = china_trend_json["list"][7]["data"][i]
                china_trend_data["累计境外输入"] = china_trend_json["list"][8]["data"][i]
                china_trend_data["新增境外输入"] = china_trend_json["list"][9]["data"][i]
                china_trend_data["新增本土"] = china_trend_json["list"][10]["data"][i]
                china_trend_data["date"] = str(date)
                self.graph.create(china_trend_data)
        print("中国历史数据更新完毕!")

    def get_global_data(self):
        # globalList  六个大洲疫情数据
        global_json = self.jsonAll["globalList"]
        neo4j_global_name = "六大洲确诊数据"
        for i in global_json:
            if i["area"] not in ["其他", "热门"]:
                time_date = self.graph.run(
                    "match (n:`六大洲确诊数据`) where n.name='" + i[
                        "area"] + "' and n.date='" + self.day_now + "' return n").data()
                if time_date:
                    continue
                else:
                    global_data = Node(neo4j_global_name, name=i["area"])
                    global_data["累计死亡"] = i["died"]
                    global_data["累计治愈"] = i["crued"]
                    global_data["累计确诊"] = i["confirmed"]
                    global_data["现有确诊"] = i["curConfirm"]
                    global_data["新增确诊"] = i["confirmedRelative"]
                    global_data["治愈率"] = i["curedPercent"]
                    global_data["死亡率"] = i["diedPercent"]
                    global_data["date"] = str(self.day_now)
                    self.graph.create(global_data)
        print("六大洲数据更新完毕!")

    def get_world_trend(self):
        # allForeignTrend 全球近三个月历史数据
        world_trend_json = self.jsonAll["allForeignTrend"]

        year = datetime.datetime.now().strftime("%Y")
        neo4j_history_name = "全球确诊历史数据"
        for i in range(len(world_trend_json["updateDate"])):
            month, day = world_trend_json["updateDate"][i].split(".")
            date = year + month + day
            time_date = self.graph.run(
                "match (n:`全球确诊历史数据`) where n.name='全球' and n.date='" + date + "' return n").data()
            if time_date:
                continue
            else:
                world_trend_data = Node(neo4j_history_name, name="全球")
                world_trend_data["累计确诊"] = world_trend_json["list"][0]["data"][i]
                world_trend_data["治愈"] = world_trend_json["list"][1]["data"][i]
                world_trend_data["死亡"] = world_trend_json["list"][2]["data"][i]
                world_trend_data["现有确诊"] = world_trend_json["list"][3]["data"][i]
                world_trend_data["新增确诊"] = world_trend_json["list"][4]["data"][i]
                world_trend_data["date"] = str(date)
                self.graph.create(world_trend_data)
        print("全球确诊历史数据更新完毕!")

    def get_world_top(self):
        # topAddCountry   每日全球新增前十
        world_top_json = self.jsonAll["topAddCountry"]
        neo4j_world_top_name = "每日全球新增前十"

        for i in world_top_json:
            time_date = self.graph.run(
                "match (n:`每日全球新增前十`) where n.name='" + i[
                    "name"] + "' and n.date='" + self.day_now + "' return n").data()
            if time_date:
                continue
            else:
                world_top_data = Node(neo4j_world_top_name, name=i["name"])
                world_top_data["新增确诊"] = i["value"]
                world_top_data["date"] = str(self.day_now)
                self.graph.create(world_top_data)
        print("每日全球新增前十数据更新完毕!")

    def get_china_overinput_top(self):
        # topOverseasInput    每日国内境外输入新增前十
        china_input_top_json = self.jsonAll["topOverseasInput"]
        neo4j_china_name = "每日国内境外输入新增前十"
        for i in china_input_top_json:
            time_date = self.graph.run(
                "match (n:`每日国内境外输入新增前十`) where n.name='" + i[
                    "name"] + "' and n.date='" + self.day_now + "' return n").data()
            if time_date:
                continue
            else:
                china_input_data = Node(neo4j_china_name, name=i["name"])
                china_input_data["境外输入"] = i["value"]
                china_input_data["date"] = str(self.day_now)
                self.graph.create(china_input_data)
        print("每日国内境外输入新增前十数据更新完毕！")

    def get_china_asymptomaticTopProvince(self):
        # asymptomaticTopProvince 每日国内无症状新增前十
        china_top_json = self.jsonAll["asymptomaticTopProvince"]
        neo4j_china_name = "每日国内无症状新增前十"
        for i in china_top_json:
            sumdata = self.graph.run(
                "match (n:`每日国内无症状新增前十`) where n.name='" + i[
                    "name"] + "' and n.date='" + self.day_now + "' return n").data()
            if sumdata:
                pass
            else:
                china_top_data = Node(neo4j_china_name, name=i["name"])
                china_top_data["新增无症状"] = i["value"]
                china_top_data["date"] = str(self.day_now)
                self.graph.create(china_top_data)
        print("每日国内无症状新增前十数据更新完毕!")

    def get_china_newAddTopProvince(self):
        # newAddTopProvince   每日国内新增前十数量
        china_top_json = self.jsonAll["newAddTopProvince"]
        neo4j_china_name = "每日国内新增前十"
        for i in china_top_json:
            sumdata = self.graph.run(
                "match (n:`每日国内新增前十`) where n.name='" + i[
                    "name"] + "' and n.date='" + self.day_now + "' return n").data()
            if sumdata:
                pass
            else:
                china_top_data = Node(neo4j_china_name, name=i["name"])
                china_top_data["本土新增"] = i["local"]
                china_top_data["境外输入"] = i["overseasInput"]
                china_top_data["date"] = str(self.day_now)
                self.graph.create(china_top_data)
        print("每日国内新增前十数据更新完成！")


if __name__ == "__main__":
    Epidemic_crawling().get_china_data()
    Epidemic_crawling().get_world_data()
    Epidemic_crawling().get_hot_words()
    Epidemic_crawling().get_china_sumdata()
    Epidemic_crawling().get_world_sumdata()
    Epidemic_crawling().get_china_trend()
    Epidemic_crawling().get_global_data()
    Epidemic_crawling().get_world_trend()
    Epidemic_crawling().get_world_top()
    Epidemic_crawling().get_china_overinput_top()
    Epidemic_crawling().get_china_asymptomaticTopProvince()
    Epidemic_crawling().get_china_newAddTopProvince()
