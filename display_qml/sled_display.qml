import QtQuick 2.15
import QtQuick.Controls 2.15


ApplicationWindow {
    visible: true
    width: 1280
    height: 800
    title: "Array Display"
    Rectangle{
        height: parent.height
        width: parent.width
        color: "#333333"
    }




    Loader{
        width: parent.width
        height: parent.height
        source: "start_pull_page.qml"
        
    }

}
