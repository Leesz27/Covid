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
function get_c1_data(){
    $.ajax({
        url:"/c1",
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
function get_c2_data(){
    $.ajax({
        url:"/c2",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            optionMap.series[0].data = data.data
            ec_center.setOption(optionMap)
        },error:function(xhr,type,errorThorwn){
            alert("地图数据显示错误!")
        }
    })
}
function get_l1_data(){
    $.ajax({
        url:"/l1",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            option_left1.xAxis.data = data.day
            option_left1.series[0].data = data.confirm
            option_left1.series[1].data = data.suspect
            option_left1.series[2].data = data.heal
            option_left1.series[3].data = data.dead
            ec_left1.setOption(option_left1)
        },error:function(xhr,type,errorThorwn){
            alert("全国累计趋势图显示错误!")
        }
    })
}
function get_l2_data(){
    $.ajax({
        url:"/l2",
        success:function(data){
            option_left2.xAxis.data = data.day
            option_left2.series[0].data = data.confirm_add
            option_left2.series[1].data = data.suspect_add
            ec_left2.setOption(option_left2)
        },error:function(xhr,type,errorThorwn){
            alert("全国新增趋势图显示错误!")
        }
    })
}
function get_r1_data(){
    $.ajax({
        url:"/r1",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            option_right1.xAxis.data = data.city
            option_right1.series[0].data = data.confirm
            ec_right1.setOption(option_right1)
        },error:function(xhr,type,errorThorwn){
            alert("条形图显示错误!")
        }
    })
}
function get_r2_data(){
    $.ajax({
        url:"/r2",
        timeout:10000,  //超时时间设置为10秒
        success:function(data){
            option_right2.xAxis.data = data.day
            option_right2.series[0].data = data.heal_add
            ec_right2.setOption(option_right2)
        },error:function(xhr,type,errorThorwn){
            alert("全国新增治愈趋势图显示错误!")
        }
    })
}

setInterval(gettime, 1000)
get_c1_data()
get_c2_data()
get_l1_data()
get_l2_data()
get_r1_data()
get_r2_data()