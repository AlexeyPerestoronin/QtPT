#include "UserHistoryModel.hpp"

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

using namespace Qt::StringLiterals;

int main(int argc, char* argv[]) {
    QGuiApplication app(argc, argv);

    // model data definitions
    UserHistoryModel userHistoryModel;

    QQmlApplicationEngine engine;
    // model data registrations
    engine.rootContext()->setContextProperty("userHistoryModel", &userHistoryModel);

    const QUrl url(u"qrc:/App/qml/main.qml"_s);
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreated,
        &app,
        [url](QObject* obj, const QUrl& objUrl) {
            if (!obj && url == objUrl)
                QCoreApplication::exit(-1);
        },
        Qt::QueuedConnection);

    engine.load(url);
    return app.exec();
}
