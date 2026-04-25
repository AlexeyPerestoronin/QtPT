#include "UserHistoryModel.hpp"

UserHistoryModel::UserHistoryModel(QObject* parent)
    : QAbstractListModel(parent) {
}

int UserHistoryModel::rowCount(const QModelIndex& parent) const {
    return _history.size();
}

QVariant UserHistoryModel::data(const QModelIndex& index, int role) const {
    if (!index.isValid() || index.row() >= _history.size())
        return {};
    if (role == TextRole)
        return _history.at(index.row());
    return {};
}

QHash<int, QByteArray> UserHistoryModel::roleNames() const {
    return {{TextRole, "text"}};
}

void UserHistoryModel::addEntry(const QString& text) {
    if (text.isEmpty())
        return;

    // always inset in the begging
    beginInsertRows(QModelIndex(), 0, 0);
    _history.prepend(text);
    endInsertRows();
}

Q_INVOKABLE void UserHistoryModel::removeEntry(int index) {
    if (index < 0 || index >= _history.size())
        return;

    beginRemoveRows(QModelIndex(), index, index);
    _history.removeAt(index);
    endRemoveRows();
}