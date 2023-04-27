var world_right2 = echarts.init(document.getElementById("r2"),"dark");

var option_right2 = {
  title: {
    text: '疫情',
    subtext: '各城市疫情',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '确诊人数',
      type: 'pie',
      radius: '50%',
      data: [],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};

world_right2.setOption(option_right2);
