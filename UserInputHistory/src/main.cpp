#include <QApplication>
#include <QLabel>
#include <QWidget>
#include <QVBoxLayout>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    // create main window
    QWidget window;
    window.setWindowTitle("Qt6 + Conan");
    window.setMinimumSize(300, 100);

    // crate label with text
    QVBoxLayout *layout = new QVBoxLayout(&window);
    QLabel *label = new QLabel("Hello World!", &window);
    label->setAlignment(Qt::AlignCenter);

    // adjust font
    QFont font = label->font();
    font.setPointSize(16);
    font.setBold(true);
    label->setFont(font);

    layout->addWidget(label);
    window.show();

    return app.exec();
}
