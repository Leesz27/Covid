// 获取后台日期时间数据
function gettime(){
    $.ajax({
        url: "/time",   //后端的服务路由
        timeout:10000,  //超时时间设置为10秒
        success:function(data){     //成功连接后台带回的日期时间放在data
            $("#time").html(data);
        },error:function(xhr, type, errorThorwn){
            alert("发送请求失败!")
        }
    })
}
function world_data(){
    $.ajax({
        url:"/world_data",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            $(".num h1").eq(0).html(data.confirm);
            $(".num h1").eq(1).html(data.suspect);
            $(".num h1").eq(2).html(data.heal);
            $(".num h1").eq(3).html(data.dead);
        },error:function(xhr, type, errorThorwn){
            alert("数字显示错误!")
        }
    })
}
function get_world_map_data(){
    $.ajax({
        url:"/world_map_data",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            optionMap.series[0].data = data.data
            world_center.setOption(optionMap)
        },error:function(xhr,type,errorThorwn){
            alert("地图数据显示错误!")
        }
    })
}
function get_world_trend_data(){
    $.ajax({
        url:"/world_trend",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            option_left1.xAxis.data = data.day
            option_left1.series[0].data = data.confirm
            option_left1.series[1].data = data.suspect
            option_left1.series[2].data = data.heal
            option_left1.series[3].data = data.dead
            world_left1.setOption(option_left1)
        },error:function(xhr,type,errorThorwn){
            alert("全球趋势图显示错误!")
        }
    })
}
function get_world_global_data(){
    $.ajax({
        url:"/world_global",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            option_left2.xAxis[0].data = data.country
            option_left2.series[0].data = data.confirm
            option_left2.series[1].data = data.heal
            world_left2.setOption(option_left2)
        },error:function(xhr,type,errorThorwn){
            alert("全国新增本土/境外图显示错误!")
        }
    })
}
function world_top_data(){
    $.ajax({
        url:"/world_top_data",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            option_right1.xAxis.data = data.city
            option_right1.series[0].data = data.confirm
            world_right1.setOption(option_right1)
        },error:function(xhr,type,errorThorwn){
            alert("条形图显示错误!")
        }
    })
}
function world_city_data(){
    $.ajax({
        url:"/world_city_data",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            option_right2.title.text = data.country+"疫情"
            option_right2.series[0].data = data.data
            world_right2.setOption(option_right2);
        },error:function(xhr,type,errorThorwn){
            alert("饼图图显示错误!")
        }
    })
}


setInterval(gettime, 1000)
world_data()
get_world_map_data()
get_world_trend_data()
get_world_global_data()
world_top_data()
world_city_data()