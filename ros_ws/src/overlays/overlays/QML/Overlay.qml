import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080 / 4
    title: "PyQt QML App"
    //flags: Qt.FramelessWindowHint
    Rectangle{
        color: "#333333"
        height: parent.height
        width: parent.width
    }
   Loader{
        y: 2*parent.height/3
        width: parent.width
        height: parent.height/3
        source: "pull_bar.qml"
        
    }
    Rectangle{
        width:parent.width/4
        height:parent.height/2
        y:0
        x:parent.width / 20
        color: "#111111"
        radius:parent.width / 50
        Text{
            x:parent.width/20
            y: 0
            text:"Team: " + dataModel.current_pull_var.team
            
            color:"#FFFFFF"
        }
        Text{
            x:parent.width/20
            y:parent.height/3
            text:"Year: " + dataModel.current_pull_var.tractor_num
            color:"#FFFFFF"
            
        }
        Text{
            x:parent.width/20
            y: 2*parent.height/3
            text:"Tractor: " + dataModel.current_pull_var.tractor_name
            color:"#FFFFFF"
            
        }

    }

    Rectangle{
        width:parent.width/5
        height:2*parent.height/3
        x:(parent.width-width)/2
        y:0
        Rectangle{
            width:parent.width
            height:parent.height/4
            color:dataModel.track_state == 1 ? "#00FF00" : dataModel.track_state == 2 ? "#FF0000" : "#FFFF00"
            Text{
                text: dataModel.track_state == 1 ? "Pulling" : dataModel.track_state == 2 ? "Stopped" : "Reseting"
                color: "#000000"
                anchors.centerIn:parent
                font.pointSize:parent.height/2.5
            }
        }
        Rectangle{
            y:parent.height/4
            width:parent.width
            height:parent.height/ 4
            color: "#555555"
            Text{
                text: dataModel.current_pull_dist.toFixed(2) + " Feet"
                color: "#FFFFFF"
                anchors.centerIn: parent
                font.pointSize:parent.height/2.5
            }

        }
        Rectangle{
            y:2*parent.height/4
            width:parent.width
            height:parent.height/ 4
            color: "#555555"
            Text{
                text: dataModel.pull_speed.toFixed(2) + " MPH"
                color: "#FFFFFF"
                anchors.centerIn: parent
                font.pointSize:parent.height/2.5
            }

        }
        Rectangle{
            y:3*parent.height/4
            width:parent.width
            height:parent.height/ 4
            color: "#555555"
            Text{
                text: dataModel.pull_force.toFixed(2) + " lb"
                color: "#FFFFFF"
                anchors.centerIn: parent
                font.pointSize:parent.height/2.5
            }

        }

        

    }
    Rectangle{
            id: rankingRect
            y:0
            width: parent.width/3
            x: 2*parent.width/3
            height: parent.height*2/3
            color: "#555555"

            Rectangle{
                width:parent.width
                height: parent.height/6
                Rectangle{
                    width:parent.width/2
                    height:parent.height
                    color: "#111111"
                    Text{
                        anchors.centerIn:parent
                        text:"Team"
                        font.pointSize: parent.height / 2.5
                        color: "#FFFFFF"
                    }
                }
                Rectangle{
                    x:parent.width/2
                    width:parent.width/4
                    height:parent.height
                    color: "#111111"
                    Text{
                        anchors.centerIn:parent
                        text:"Distance"
                        font.pointSize: parent.height / 2.5
                        color: "#FFFFFF"
                    }
                }
                Rectangle{
                    x: 3*parent.width/4
                    width:parent.width/4
                    height:parent.height
                    color: "#111111"
                    Text{
                        anchors.centerIn:parent
                        text:"Max Speed"
                        font.pointSize: parent.height / 2.5
                        color: "#FFFFFF"
                    }
                }
            }
            ListView{
                id: lastpullsview
                width:parent.width
                height:5*rankingRect.height /6
                y:rankingRect.height/6
                model:dataModel.last_pulls_qt
                //spacing: 10
                orientation: ListView.Vertical
                delegate: Rectangle{
                    width:lastpullsview.width
                    height:lastpullsview.height/6
                    
                    Rectangle{
                        width: parent.width/2
                        color:"#555555"
                        height:parent.height
                        Text{
                            text: modelData.team_name
                            color: "#FFFFFF"
                            font.pointSize: parent.height/2.5
                        }
                    }
                    Rectangle{
                        x:parent.width/2
                        width: parent.width/4
                        color:"#555555"
                        height:parent.height
                        Text{
                            text: modelData.distance
                            color: "#FFFFFF"
                            font.pointSize: parent.height/2.5
                        }
                    }
                    Rectangle{
                        x:3*parent.width/4
                        width: parent.width/4
                        color:"#555555"
                        height:parent.height
                        Text{
                            text: modelData.speed
                            color: "#FFFFFF"
                            font.pointSize: parent.height/2.5
                        }
                    }
                }
            } 
            
        }
    
}
