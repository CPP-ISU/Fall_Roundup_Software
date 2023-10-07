import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    id:root
    width: 3840
    height: 600
    title: "Pull Overlay"
    property string team:"Iowa State"
    property string track_state: "Reseting"
    property int current_dist: 1234
    property int max_speed: 75
    Rectangle{
        x:0
        y:0
        width:root.width
        height:root.height
        color:"#505050"
        Rectangle{
            id:track_state_display
            width:parent.width/3
            height:parent.height/4
            anchors.horizontalCenter:parent.horizontalCenter
            anchors.top:parent.top
            color: (track_state=="Pulling") ? "#00ff00" : "#ff0000" 
            Text{
                anchors.horizontalCenter:parent.horizontalCenter
                anchors.verticalCenter:parent.verticalCenter
                font.pointSize:root.width*50/3840
                text: track_state
                color: "#FFFFFF"
            }
        }
        Rectangle{
            id:current_pull_display
            anchors.horizontalCenter:parent.horizontalCenter
            y:parent.height/4
            height:parent.height*3/4
            width:root.width/3
            color: "#333333"

            Text{
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top:parent.top
            font.pointSize:root.height*50/600
            text:team
            color: "#FFFFFF"
            }
            Text{
                anchors.horizontalCenter:parent.horizontalCenter
                y:parent.height/4*2
                text: current_dist/10 +" ft"
                font.pointSize: root.height/600 * 50
                color: "#FFFFFF"
            }
            Text{
                x:parent.width/10
                y:parent.height/2
                text: max_speed/10 
                font.pointSize:root.height/600 * 50
                color: "#FFFFFF"
            }
        }

        Image {
            source: "http://localhost:5000/Overlay_Ranking"  // Replace with your Flask server's image route
            x:root.width/3 *2
            y:0
            id:leaderboard
            Timer {
            interval: 60000  // Set the interval in milliseconds (e.g., 5000 = 5 seconds)
            repeat: true
            running: true
            onTriggered: {
                console.log("Timer triggered. Reloading image...");
                // Reload the image by changing the source URL
                leaderboard.source = "http://localhost:5000/Overlay_Ranking" + "?timestamp=" + new Date().getTime();
            }
        }
        }

        ListView {
            model: dataWrapper.dataList
            width:parent.width/3
            height:parent.height
            delegate: Item {
            width: parent.width
            height: 50
            Text {
                text: {
                var team = model.team;
                var distance = model.distance;
                console.log("Team:", team, "Distance:", distance);
                return "Team: " + team + ", Distance: " + distance;
            }
                //text: "Team: " + model.team + ", Distance: " + model.distance
        }
    }
}

Component.onCompleted: {
    // Force a refresh of the ListView
    currentIndex = -1;
    currentIndex = 0;
}

    }
    
}

