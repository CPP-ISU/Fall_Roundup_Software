import QtQuick 2.15
import QtQuick.Controls 2.15


Rectangle{
    id: root
    height: parent.height
    width: parent.width
    color: "#333333"
    property int team_id:0
    property int tractor_id:0
    property int pull_id:0
    property var hitch_height: 7.5
    property var sled_height: 1.5
    property var class_id: 0
    Text{
        text: "Start Pull"
        x: parent.width / 30
        y:parent.height / 30
        font.pointSize: 30
        color: "white"
    }
    Text{
        text: "Team"
        x: 3*parent.width / 30
        y: 7*parent.height / 30
        font.pointSize: 30
        color: "white"
    }
    Text{
        text: "Tractor"
        x: 13*parent.width / 30
        y: 7*parent.height / 30
        font.pointSize: 30
        color: "white"
    }
    Text{
        text: "Pull"
        x: 23*parent.width / 30
        y: 7*parent.height / 30
        font.pointSize: 30
        color: "white"
    }
    ListView {
        id: listView
        width: parent.width/3
        height: 2*parent.height/3
        model: dataModel.data
        y: parent.height/3
        x:0

        delegate: Item {
            width: listView.width
            height: 50

            Rectangle {
                width: parent.width
                height: 50
                color: root.team_id==modelData.team_id ? "darkgrey":"lightgrey"
                radius: 10
                Text {
                    anchors.centerIn: parent
                    text: modelData.team_abrev
                }
                Button{
                    opacity: 0
                    width:parent.width
                    height: parent.height
                    onClicked: {
                        tractorlistView.model=modelData.tractors;
                        root.team_id=modelData.team_id;
                    }
                    
                }
            }
        }
    }
    ListView {
        id: tractorlistView
        width: parent.width/3
        height: 2*parent.height/3
        
        y: parent.height/3
        x: parent.width/3
        delegate: Item {
            width: listView.width
            height: 50

            Rectangle {
                width: parent.width
                height: 50
                color: root.tractor_id==modelData.tractor_id ? "darkgrey":"lightgrey"
                radius: 10
                Text {
                    anchors.centerIn: parent
                    text: modelData.tractor_num
                }
                Button{
                    opacity: 0
                    width:parent.width
                    height: parent.height
                    onClicked: {
                                pulllistView.model=modelData.pulls;
                                root.tractor_id=modelData.tractor_id;
                    }
                    
                }
            }
        }
    }
    ListView {
        id: pulllistView
        width: parent.width/3
        height: parent.height/3
        
        y: parent.height/3
        x: 2*parent.width/3
        delegate: Item {
            width: listView.width
            height: 50

            Rectangle {
                width: parent.width
                height: 50
                color: root.pull_id==modelData.pull_id ? "darkgrey":"lightgrey"
                radius: 10
                Text {
                    y:20
                    x: parent.width/3
                    
                    text: modelData.hook_num
                }
                Text {
                    y: 20
                    x: 2*parent.width/3
                    
                    text: modelData.dist
                }
                Button{
                    opacity: 0
                    width:parent.width
                    height: parent.height
                    onClicked: {root.pull_id=modelData.pull_id;
                                
                    }
                    
                    
                }
            }
        }
    }

    Button{
        x: 15*parent.width/20
        y: 17*parent.height/20
        width: parent.width/5
        height: 2*parent.height/20
        onClicked: {
            var array = [root.class_id, root.team_id,root.tractor_id,root.pull_id];
            dataModel.start_pull(array);
        }
        Text{
            anchors.centerIn: parent
            text: "Start"
        }
    }

    Button{
        x: 5*parent.width/20
        y: 17*parent.height/20
        width: parent.width/5
        height: 2*parent.height/20
        onClicked: {
            
            dataModel.update_list();
        }
        Text{
            anchors.centerIn: parent
            text: "Update"
        }
    }

    Connections {
    target: dataModel
    onDataChanged: {
        listView.model = dataModel.data;
        console.log("Data changed");
    }
    }
    ComboBox {
    width: 200
    model: [ 7, 7.5, 8, 8.5, 9, 9.5 ]
    onAccepted: {
        root.hitch_height=get(currentIndex)
    }
    }
}
