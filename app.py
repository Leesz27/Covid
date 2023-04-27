from flask import Flask, jsonify
from flask import render_template
import datetime
import utils_neo4j
import utils
# from flask_cors import CORS
from flask import request

# 创建一个flask实例
app = Flask(__name__)

# CORS(app)  # , supports_credentials=True)


@app.route('/', methods=["get", "post"])
def china_view():
    return render_template("china.html")


# 右上角时间模块
@app.route('/time', methods=["get", "post"])
def time():
    return utils.get_time()


# 正中间 四个数字显示模块
@app.route('/c1', methods=['get', 'post'])
def data_view():
    data = utils.get_c1_data()
    # 转换为json数据（字典）
    return jsonify({"confirm": str(data[0]), "suspect": str(data[1]), "heal": str(data[2]), "dead": str(data[3])})


# 地图显示模块
@app.route('/c2', methods=['get', 'post'])
def china_map():
    res = []
    for i in utils.get_c2_data():
        # print(i)
        res.append({"name": i[0], "value": int(i[1])})
    return jsonify({"data": res})


# 左上角模块
@app.route('/l1', methods=['get', 'post'])
def new_add_confirm():
    data = utils.get_l1_data()
    # 定义五个列表
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for a, b, c, d, e in data:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


# 左下角模块，显示
@app.route('/l2', methods=['get', 'post'])
def new_add_local():
    data = utils.get_l2_data()
    # 定义五个列表
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})


# 右上角模块
@app.route('/r1', methods=['get', 'post'])
def new_add_top():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k, v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})


# 12、调用utils中的数据库函数get_r2_data,在py注册新路由r2
@app.route('/r2', methods=['get', 'post'])
def world_pie():
    data = utils.get_r2_data()
    # 定义两个列表
    day, heal_add = [], []
    for a, b in data:
        day.append(a.strftime("%m-%d"))
        heal_add.append(b)

    return jsonify({"day": day, "heal_add": heal_add})


@app.route('/world', methods=["get", "post"])
def world_view():
    return render_template("world.html")


# 地图显示模块
@app.route('/world_map_data', methods=['get', 'post'])
def world_map():
    data = []
    world_data = utils_neo4j.neo4j().get_world_map_data()
    for i in world_data:
        data.append({"name": i[0], "value": int(i[1])})
    return jsonify({"data": data})


# 正中间 四个数字显示模块
@app.route('/world_data', methods=['get', 'post'])
def world_data():
    data = utils_neo4j.neo4j().get_world_data()
    # 转换为json数据（字典）
    return jsonify({"confirm": str(data[0]), "suspect": str(data[1]), "heal": str(data[2]), "dead": str(data[3])})


# 左上角模块
@app.route('/world_trend', methods=['get', 'post'])
def get_world_trend_data():
    data = utils_neo4j.neo4j().get_world_trend_data()
    # 定义五个列表
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for i in data:
        value = i["n"]
        date = datetime.datetime.strptime(value["date"], "%Y%m%d").strftime("%m-%d")
        day.append(date)
        confirm.append(value["累计确诊"])
        suspect.append(value["现有确诊"])
        heal.append(value["治愈"])
        dead.append(value["死亡"])
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


# 左下角模块
@app.route('/world_global', methods=['get', 'post'])
def get_world_global_data():
    data = utils_neo4j.neo4j().get_world_global_data()
    country = []
    confirm = []
    heal = []
    for i in data:
        value = i["n"]
        country.append(value["name"])
        confirm.append(value["累计确诊"])
        heal.append(value["累计治愈"])
    return jsonify({"country": country, "confirm": confirm, "heal": heal})


# 右上角模块
@app.route('/world_top_data', methods=['get', 'post'])
def world_top_data():
    data = utils_neo4j.neo4j().get_world_top_data()
    country = []
    confirm = []
    for i in data:
        value = i["n"]
        country.append(value["name"])
        confirm_add = int(value["新增确诊"])
        confirm.append(confirm_add)
    return jsonify({"city": country, "confirm": confirm})


# 12、调用utils中的数据库函数get_r2_data,在py注册新路由r2
@app.route('/world_city_data', methods=['get', 'post'])
def get_world_city_data():
    country, data = utils_neo4j.neo4j().get_world_city_data()
    top_data = []
    for i in data[:10]:
        top_data_dict = {"name": i[0], "value": int(i[1])}
        top_data.append(top_data_dict)
    return jsonify({"data": top_data, "country": country})


@app.route('/china_city_data', methods=['get', 'post'])
def get_china_city_data():
    country, data = utils_neo4j.neo4j().get_world_city_data()
    top_data = []
    for i in data[:10]:
        top_data_dict = {"name": i[0], "value": int(i[1])}
        top_data.append(top_data_dict)
    return jsonify({"data": top_data, "country": country})


@app.route('/search_data', methods=['GET', 'POST'])
def get_search_data():
    country = request.args.get("type")
    city = request.args.get("region")
    country_data = utils_neo4j.neo4j().get_search_data(country=country, city=city)
    country_list = []
    for i in country_data:
        country_list.append([i["m"]["city_name"], i["m"]["累计确诊"], i["m"]["累计治愈"], i["m"]["累计死亡"], i["m"]["新增确诊"]])
    return jsonify({"data": country_list})


# 按间距中的绿色按钮以运行脚本
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999, debug=True)
