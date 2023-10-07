import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Shapes 1.15
import "Gauge_box.qml" as Gauge_box

Item {
    width: 300
    height: 300
    property double max: 10
    property double min: 0
    property double val: 7.25
    property string name: "Speed"
    property string unit: "MPH"
    property bool highWaterTickEnabled:true
    property double highwaterMark:8

    id:root
    Gauge_box{
        hc:parent.width/2
        vc:parent.height/2
        width:parent.width
        height:parent.height



        Shape {

            width: parent.width
            height: parent.height
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: parent.height/10
            // multisample, decide based on your scene settings
            layer.enabled: true
            layer.samples: 4

            ShapePath {

                fillColor: "#666666"
                strokeColor: "#FF0000"


                strokeWidth: root.width*20/300
                capStyle: ShapePath.FlatCap



                PathAngleArc {
                    centerX: root.width/2; centerY: root.height/2
                    radiusX: root.width/3; radiusY: root.width/3
                    startAngle: -225+(270*highwaterMark/(max-min))
                    sweepAngle: 4
                }
            }
            ShapePath {
                
                strokeColor: "#11cc11"


                strokeWidth: root.width*20/300
                capStyle: ShapePath.FlatCap



                PathAngleArc {
                    centerX: root.width/2; centerY: root.height/2
                    radiusX: root.width/3; radiusY: root.width/3
                    startAngle: -225
                    sweepAngle: 270*(val/(max-min))
                }
            }

        }
        Text{
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            text:val
            color: "#FFFFFF"
            font.pointSize: 60/300*parent.width
        }
        Text{
            font.pointSize: root.width*40/300
            text:name
            color:"#FFFFFF"
            anchors.horizontalCenter: parent.horizontalCenter
        }
        Text{
            font.pointSize: root.width*40/300
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: root.height/5
            text: unit
            color:"#FFFFFF"
        }
        Text{
            text:highwaterMark

        }
    }
}
