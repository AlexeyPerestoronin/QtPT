#pragma once

#include <QAbstractListModel>
#include <QStringList>

class UserHistoryModel : public QAbstractListModel {
    Q_OBJECT

    public:
    enum HistoryRoles
    {
        TextRole = Qt::UserRole + 1
    };

    explicit UserHistoryModel(QObject* parent = nullptr);

    int rowCount(const QModelIndex& parent = QModelIndex()) const override;
    QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

    Q_INVOKABLE void addEntry(const QString& text);
    Q_INVOKABLE void removeEntry(int index);

    private:
    QStringList _history;
};
