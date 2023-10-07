import QtQuick 2.15
import QtQuick.Controls 2.15


Rectangle {

    property int hc: 50
    property int vc: 50
    width: 100
    height: 100
    radius: width / 10
    x:hc-(width/2)
    y:vc-(height/2)
    

    Rectangle {
        width: parent.width * 19 / 20
        height: parent.height * 19 / 20
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        radius: parent.radius
        
    }
}
