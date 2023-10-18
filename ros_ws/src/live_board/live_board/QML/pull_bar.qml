import QtQuick 2.15
import QtQuick.Controls 2.15

Item{
    id: root
    Rectangle{
        width:17*parent.width/20
        height: parent.height/2
        x:(parent.width-width)/2
        y:(parent.height-height)/2
        color:"#111111"
        id:track
    }
        Repeater{
            width: parent.width
            height: parent.height
            model: dataModel.data
            delegate: 
            Item{
                width:parent.width
                height:parent.height
                Rectangle{
                    width: parent.width/100
                    height:track.height
                    x:track.x + track.width- (modelData.dist/dataModel.max_pull_dist)*track.width
                    y: track.y
                    color:modelData.color
                }
                Text{
                    text:modelData.team
                    color:modelData.color
                    x:track.x + track.width- (modelData.dist/dataModel.max_pull_dist)*track.width
                    y:track.y + track.height
                    font.pointSize: parent.height/20
                }
                Text{
                    text: modelData.dist
                    color:"#FFFFFF"
                    x:track.x + track.width- (modelData.dist/dataModel.max_pull_dist)*track.width
                    y:track.y - parent.height/5
                    font.pointSize: parent.height/20
                }
            }
        }

        Rectangle{
            property int var_width: (dataModel.current_pull_dist/dataModel.max_pull_dist)*track.width
            x:track.x+track.width-var_width
            y:track.y
            width: var_width
            height: track.height
            color: "#00FF00"
            opacity: .5
        }
    

}
