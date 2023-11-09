import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080
    title: "Leader Board"
    id: root

    Rectangle {
        width: parent.width
        height: parent.height
        color: "#444444"
    }

    Row{
        Rectangle{
            width:root.width
            height:root.height
            Rectangle{
                width:parent.width
                height:parent.height/16
                color: "#222222"
                Text{
                    anchors.centerIn: parent
                    text:dataModel.leaderBoard[5].class_name
                    font.pointSize: parent.height / 3
                    color: "#FFFFFF"
                }
            }
            Rectangle{
                width:parent.width
                height:parent.height/16
                y:height
                Rectangle{
                    width:parent.width/3
                    height: parent.height
                    color: "#333333"
                    Text{
                        anchors.centerIn: parent
                        text: "Team"
                        color: "#FFFFFF"
                        font.pointSize: parent.width/15
                    }
                }
                Rectangle{
                    x:parent.width/3
                    width:parent.width/6
                    height: parent.height
                    color: "#333333"
                    Text{
                        anchors.centerIn: parent
                        text: "Tractor"
                        color: "#FFFFFF"
                        font.pointSize: parent.width/7.5
                    }
                }
                Rectangle{
                    x:parent.width/3+parent.width/6
                    width:parent.width/6
                    height: parent.height
                    color: "#333333"
                    Text{
                        anchors.centerIn: parent
                        text: "Dist"
                        color: "#FFFFFF"
                        font.pointSize: parent.width/7.5
                    }
                }
                Rectangle{
                    x:parent.width/3+parent.width*2/6
                    width:parent.width/3
                    height: parent.height
                    color: "#333333"
                    Text{
                        anchors.centerIn: parent
                        text: "Speed"
                        color: "#FFFFFF"
                        font.pointSize: parent.width/15
                    }
                }
            }
        ListView{
            y:parent.height/8
            id:listView1
            model:dataModel.leaderBoard[5].pulls
            width:parent.width
            height:parent.height
            delegate:Rectangle{
                color:"#FF0000"
                width:listView1.width
                height: listView1.height / dataModel.leaderBoard[5].pulls.length
                Rectangle{
                    width:parent.width/3
                    height:parent.height
                    color: "#222222"
                    Text{
                        anchors.centerIn: parent
                        text:modelData.team_abv
                        font.pointSize: parent.width/15
                        color: "#FFFFFF"
                    }
                }
                Rectangle{
                    x:parent.width/3
                    width:parent.width/6
                    height:parent.height
                    color: "#222222"
                    Text{
                        anchors.centerIn: parent
                        text:modelData.tractor_num
                        font.pointSize: parent.width/7.5
                        color: "#FFFFFF"
                    }
                }
                Rectangle{
                    x:parent.width/3 +parent.width/6 + parent.width/6
                    width:parent.width/3
                    height:parent.height
                    color: "#222222"
                    Text{
                        anchors.centerIn: parent
                        text:modelData.speed.toFixed(2)
                        font.pointSize: parent.width/15
                        color: "#FFFFFF"
                    }
                }
                Rectangle{
                    x:parent.width/3 +parent.width/6
                    width:parent.width/6
                    height:parent.height
                    color: "#222222"
                    Text{
                        anchors.centerIn: parent
                        text:modelData.distance.toFixed(2)
                        font.pointSize: parent.width/7.5
                        color: "#FFFFFF"
                    }
                }
                
            }
        }
        }
    }
}
