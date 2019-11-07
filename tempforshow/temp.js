var chart = Highcharts.chart('container', {
    chart: {
        type: 'bar'
    },
    title: {
        text: '词对图'
    },
    subtitle: {
        text: '数据来源: DMAN'
    },
    xAxis: {
        categories: ['police', 'protesters', 'said', 'antielab', 'rd', 'hk', 'people', 'one', 'kong',
            'hong', 'station', 'riot', 'wan', 'man', 'officers', 'tear', 'two', 'carrielam', 'st', 'gas'],
        title: {
            text: null
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '提及次数',
            align: 'high'
        },
        labels: {
            overflow: 'justify'
        }
    },
    tooltip: {
        valueSuffix: ' 次'
    },
    plotOptions: {
        bar: {
            dataLabels: {
                enabled: true,
                allowOverlap: false // 允许数据标签重叠
            }
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -40,
        y: 100,
        floating: true,
        borderWidth: 1,
        backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
        shadow: true
    },
    series: [{
        name: 'times',
        data: [1083, 603, 596, 477, 472, 366, 311, 310, 308, 287, 285, 274, 205, 199, 185, 172, 165, 162, 160, 159]}]
});