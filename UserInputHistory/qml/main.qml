import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 400
    height: 500
    title: "QML Input History"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // user input
        TextField {
            id: textField
            placeholderText: "Введите текст..."
            Layout.fillWidth: true
        }

        // accept button
        Button {
            text: "Добавить в историю"
            Layout.fillWidth: true
            onClicked: {
                userHistoryModel.addEntry(textField.text)
                textField.text = ""
            }
        }

        // user input history
        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: userHistoryModel
            delegate: ItemDelegate {
                width: listView.width

                contentItem: RowLayout {
                    spacing: 10

                    Button {
                        text: "❌"
                        flat: true // remove border around button
                        Layout.preferredWidth: 25
                        Layout.alignment: Qt.AlignVCenter
                        onClicked: {
                            userHistoryModel.removeEntry(index)
                        }
                    }

                    Label {
                        text: model.text
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                background: Rectangle {
                    color: index % 2 === 0 ? "#f9f9f9" : "#ffffff"
                    border.color: "#eeeeee"
                    radius: 4
                }
            }
        }
    }
}
