import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1280
    height: 800
    title: "PyQt QML App"
    id: window
    property bool start_enabled: false
    Rectangle{
        width:parent.width
        height: parent.height
        color: "#555555"
        Loader{
            y: 3*parent.height/4
            width: parent.width
            height: parent.height/4
            source: "pull_bar.qml"
        
        }

        Loader{
            height: parent.height/1.5
            width: parent.width/1.75
            y:parent.height/14
            x:parent.width/2 - width/2
            source: "pul_chart.qml"
        } 

        Rectangle{
            height: parent.height/15
            width: parent.width /5
            y:0
            x:parent.width/2 -width/2
            color: dataModel.track_state == 1 ? "#00FF00" : dataModel.track_state == 2 ? "#FF0000" : "#FFFF00"
            Text{
                anchors.centerIn: parent
                font.pointSize: parent.height /3
                text: dataModel.track_state == 1 ? "Pulling" : dataModel.track_state == 2 ? "Stopped" : "Resetting"
            }
        }
        Rectangle{
            height: parent.height/15
            width: parent.width /2.5
            y:0
            x:0
            color: "#333333"
            Text{
                anchors.centerIn: parent
                font.pointSize: parent.height /3
                text: "Class: " + dataModel.current_class_name
                color: "#FFFFFF"
            }
        }
        Rectangle{
            height:parent.height/15
            width: parent.width/ 2.5
            x:6*parent.width / 10
            y:0
            color: "#333333"
            Text{
                anchors.centerIn:parent
                font.pointSize: parent.height/ 3
                text: dataModel.current_pull_var.team + " " + dataModel.current_pull_var.tractor_num
                color: "#FFFFFF"
            }
        }


        Loader{

            height:parent.height/3
            width:parent.height/3
            x:parent.width/64
            y:2*parent.height/8 - height/2
            source: "Gauge.qml"
            property var val:dataModel.pull_speed
            property double max: 12
            property double min: 0
            property string name: "Speed"
            property string unit: "MPH"
            property bool highWaterTickEnabled:true
            property double highwaterMark:dataModel.maxSpeed

        }
        Loader{

            height:parent.height/3
            width:parent.height/3
            x:parent.width/64
            y:2*parent.height/8 - height/2 + parent.height / 3
            source: "Gauge.qml"
            property var val:dataModel.currentPower
            property double max: 31
            property double min: 0
            property string name: "Power"
            property string unit: "HP"
            property bool highWaterTickEnabled:true
            property double highwaterMark:dataModel.maxPower

        }
        Loader{

            height:parent.height/3
            width:parent.height/3
            x:63*parent.width/64 - width
            y:2*parent.height/8 - height/2
            source: "Gauge.qml"
            property var val:dataModel.pull_force
            property double max: 2500
            property double min: 0
            property string name: "Force"
            property string unit: "lb"
            property bool highWaterTickEnabled:true
            property double highwaterMark:dataModel.maxForce

        }
        Loader{

            height:parent.height/3
            width:parent.height/3
            x:63*parent.width/64 - width
            y:2*parent.height/8 - height/2 + parent.height / 3
            source: "Gauge.qml"
            property var val:dataModel.current_pull_dist
            property double max: dataModel.max_pull_dist
            property double min: 0
            property string name: "Distance"
            property string unit: "ft"
            property bool highWaterTickEnabled:false
            property double highwaterMark:dataModel.maxSpeed

        }

    Button{
        width:parent.width
        height:parent.height
        opacity:0
        onClicked:window.start_enabled=true
    }

    Loader{
        width: parent.width
        height: parent.height
        source: "start_pull_page.qml"
        visible:window.start_enabled
        Connections{
            //target: item
            onDisableStart:{
                window.start_enabled=false;
            }
        }
        
    }
    /*Button{
        width:parent.width/8
        height:parent.height/8
        x:17*parent.width/20
        y:15*parent.height/20
        onClicked:window.start_enabled=false
        Text{
            text:"Exit"
        }
    }*/
        

    }
}