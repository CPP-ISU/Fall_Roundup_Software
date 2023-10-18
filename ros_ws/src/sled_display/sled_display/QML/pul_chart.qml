import QtQuick 2.15
import QtQuick.Controls 2.15
import QtCharts 2.15

Item{
    id:root
    property var maxxaxis1: dataModel.pullDuration
    property var max_y_axis_1: dataModel.maxSpeed*1.1
    
    property var max_y_axis_2: dataModel.maxForce*1.1


    Rectangle{
        id: graph
        height:7*parent.height/8
        width:3*parent.width /4
        x:parent.width/2 - width/2
        border.color: "#888888"
        border.width: 5
        y:0
        color: "#FFFFFF"
        Repeater{
            model:dataModel.chartData
            Rectangle{
                height:4*graph.height/500
                width: 4*graph.height/500
                color: "#0000FF"
                x: modelData.time / root.maxxaxis1 * graph.width
                y: graph.height - modelData.speed / root.max_y_axis_1 * graph.height
            }
        }

        Repeater{
            model:dataModel.chartData
            Rectangle{
                height: 4*graph.height/500
                width: 4*graph.height/500
                color: "#FF0000"
                x: modelData.time / root.maxxaxis1 * graph.width
                y: graph.height - modelData.force / root.max_y_axis_2 * graph.height
            }
        }


    }
    Rectangle{
        x:0
        y:0
        height:7*parent.height/8
        width: parent.width/8
        color: "#FFFFFF"
        Rectangle{
            x:parent.width/2
            y:parent.height/6
            height:parent.height/10
            width:parent.height/10
            color: "#0000FF"
        }
        Text{
            x:-1*parent.width/2
            y:parent.height*2/4
            text:"Speed (MPH)"
            rotation: 270
        }
        Rectangle{
            x:parent.width*3/4
            height:parent.height/50
            width:parent.width/4
            color: "#000000"
        }
        Text{
            text:max_y_axis_1.toFixed(0)
            x: parent.width/4
        }
        Text{
            y: parent.height/2
            text:(max_y_axis_1/2).toFixed(0)
            x: 2*parent.width/4
        }
        Rectangle{
            x:parent.width*3/4
            height:parent.height/50
            width:parent.width/4
            y:parent.height/2 -height
            color: "#000000"
        }
        Rectangle{
            x:parent.width*3/4
            height:parent.height/50
            width:parent.width/4
            y:parent.height-height
            color: "#000000"
        }
        Text{
            text:"0"
            y: 7.5*parent.height/8
            x: parent.width/4
        }
    }
    Rectangle{
        x:parent.width*7/8
        y:0
        height:7*parent.height/8
        width: parent.width/8
        color: "#FFFFFF"
        Rectangle{
            x:parent.width/8
            y:parent.height/6
            height:parent.height/10
            width:parent.height/10
            color: "#FF0000"
        }
        Text{
            x:parent.width/4
            y:parent.height*2/4
            text:"Force (lb)"
            rotation: 270
        }
        Rectangle{
            height:parent.height/50
            width:parent.width/4
            color: "#000000"
        }
        Text{
            text:max_y_axis_2.toFixed(0)
            x: parent.width/4
        }
        Text{
            y: parent.height/2
            text:(max_y_axis_2/2).toFixed(0)
            x: parent.width/4
        }
        Rectangle{
            
            height:parent.height/50
            width:parent.width/4
            y:parent.height/2 -height
            color: "#000000"
        }
        Rectangle{
            
            height:parent.height/50
            width:parent.width/4
            y:parent.height-height
            color: "#000000"
        }
        Text{
            text:"0"
            y: 7.5*parent.height/8
            x: parent.width/4
        }

    }
    Rectangle{
        y: 7*parent.height/8
        color:"#FFFFFF"
        width:parent.width
        height: parent.height/8
        Text{
            x:parent.width/8
            y:parent.height/2
            text: "0"
        }
        Text{
            x:7*parent.width/8
            y:parent.height/2
            text: maxxaxis1.toFixed(0)
        }

        Rectangle{
            height:parent.height/3
            width:parent.width/100
            x:parent.width/8
            color: "#000000"
        }
        Rectangle{
            height:parent.height/3
            width:parent.width/100
            x:parent.width/2 - width/2
            color: "#000000"
        }
        Rectangle{
            height:parent.height/3
            width:parent.width/100
            x:7*parent.width/8 -width
            color: "#000000"
        }


        Text{
            text:"Time (s)"
            anchors.centerIn:parent
        }
    }
    
}

/*ListView{
        height:parent.height
        width: parent.width
        model:dataModel.chartData
        delegate:{
            Text{
                text:modelData.speed
            }
        }
    }*/

