import QtQuick 2.15
import QtQuick.Controls 2.15
import QtCharts 2.3

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Qt Charts Example"

    ChartView {
        width: parent.width
        height: parent.height
        antialiasing: true

        Component.onCompleted: {
            // Create a line series
            
            for (var i = 0; i < chartData.data.length; i++) {
                series.append(i, chartData.data[i])
            }

            // Create a chart and add the series
            var chart = QtCharts.QChart()
            chart.addSeries(series)

            // Create axes and add them to the chart
            var axisX = QtCharts.QValueAxis()
            var axisY = QtCharts.QValueAxis()
            chart.addAxis(axisX, Qt.AlignBottom)
            chart.addAxis(axisY, Qt.AlignLeft)
            series.attachAxis(axisX)
            series.attachAxis(axisY)

            // Set the chart title
            chart.setTitle("Dynamic Line Chart")

            // Set the chart to the ChartView
            chartView.chart = chart
        }
    }
}
