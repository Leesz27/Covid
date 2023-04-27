var world_left2 = echarts.init(document.getElementById("l2"),"dark");

var option_left2 = {
   tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      crossStyle: {
        color: '#999'
      }
    }
  },
  legend: {
    data: ['累计确诊','累计治愈']
  },
  xAxis: [
    {
      type: 'category',
      data: [],
      axisPointer: {
        type: 'shadow'
      }
    }
  ],
  yAxis: [
    {
      type: 'value',
      name: '累计确诊',

      formatter: function(value) {
        if (value >= 100000) {
            value = value / 1000000 + 'k';
        }
        return value;
        },
      axisLabel: {
        formatter: '{value} k'
      }
    },
    {
      type: 'value',
      name: '累计治愈',

      formatter: function(value) {
        if (value >= 100000) {
            value = value / 1000000 + 'k';
        }
        return value;
        },
      axisLabel: {
        formatter: '{value} k'
      }
    },
  ],
  series: [
    {
      name: '累计确诊',
      type: 'bar',
      tooltip: {
        valueFormatter: function (value) {
          return value;
        }
      },
      data: []
    },
    {
      name: '累计治愈',
      type: 'line',
      yAxisIndex: 1,
      tooltip: {
        valueFormatter: function (value) {
          return value;
        }
      },
      data: []
    }
  ]
};

world_left2.setOption(option_left2);
