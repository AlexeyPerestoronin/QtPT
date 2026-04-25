import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 400
    height: 500
    title: "QML Input History"

    // Модель данных для списка
    ListModel {
        id: historyModel
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // Поле ввода
        TextField {
            id: textField
            placeholderText: "Введите текст..."
            Layout.fillWidth: true
            onAccepted: addItem() // Добавление по нажатию Enter
        }

        // Кнопка
        Button {
            text: "Добавить в историю"
            Layout.fillWidth: true
            highlighted: true
            onClicked: addItem()
        }

        // Список (ListView)
        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: historyModel
            clip: true
            
            delegate: ItemDelegate {
                width: parent.width
                text: model.text
                background: Rectangle {
                    color: index % 2 === 0 ? "#f9f9f9" : "#ffffff"
                    border.color: "#eeeeee"
                }
            }
        }
    }

    // Функция добавления элемента
    function addItem() {
        if (textField.text !== "") {
            historyModel.insert(0, {"text": textField.text}); // Добавляем в начало
            textField.text = ""; // Очищаем поле
        }
    }
}
