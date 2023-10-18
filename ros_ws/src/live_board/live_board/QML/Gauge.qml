import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Shapes 1.15


Item {
    width: parent.width
    height: parent.height
    property double max: parent.max
    property double min: parent.min
    property double val: parent.val
    property string name: parent.name
    property string unit: parent.unit
    property bool highWaterTickEnabled:parent.highWaterTickEnabled
    property double highwaterMark:parent.highwaterMark

    id:root
    Rectangle{
        //hc:parent.width/2
        //vc:parent.height/2
        width:parent.width
        height:parent.height
        color: "#444444"
        radius:30
        border.width:6
        border.color: "#777777"



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

                fillColor: "#444444"
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
            text:val.toFixed(2)
            color: "#FFFFFF"
            font.pointSize: 15/300*parent.width
        }
        Text{
            font.pointSize: root.width*18/300
            text:name
            color:"#FFFFFF"
            anchors.horizontalCenter: parent.horizontalCenter
        }
        Text{
            //font.pointSize: root.width*40/300
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: root.height/5
            text: unit
            color:"#FFFFFF"
        }
        Text{
            //font.pointSize: root.width*40/300
            visible:root.highWaterTickEnabled
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: root.height/3
            text: highwaterMark.toFixed(2)
            color:"#FFFFFF"
        }
    }
}
