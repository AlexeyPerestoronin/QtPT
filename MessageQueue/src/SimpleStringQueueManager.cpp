#include <MessageQueue/SimpleStringQueueManager.hpp>

#include <mutex>

namespace MessageQueue {

std::mutex ReceiveMessageAccess{};

SimpleStringQueueManager::SimpleStringQueueManager(AMQP::Address address, std::string queueName)
    : _queueHandler{std::move(address),
                    std::move(queueName),
                    [&](std::string message)
                    {
                        auto lock = std::lock_guard<std::mutex>(ReceiveMessageAccess);
                        this->_receivedMessage.push_back(std::move(message));
                    }} {
}

void SimpleStringQueueManager::publish(const std::string& message) {
    std::string defaultExchange{""};
    _queueHandler.publish(defaultExchange, message);
}

std::optional<std::string> SimpleStringQueueManager::consume() {
    auto lock = std::lock_guard<std::mutex>(ReceiveMessageAccess);
    if (!_receivedMessage.empty()) {
        auto message = _receivedMessage.front();
        _receivedMessage.pop_front();
        return message;
    }

    return std::nullopt;
}

} // namespace MessageQueue
