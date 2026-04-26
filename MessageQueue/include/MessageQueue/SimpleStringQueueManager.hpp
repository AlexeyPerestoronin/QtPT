#pragma once

#include "AmqpQueueHandler.hpp"

#include <list>
#include <optional>

namespace MessageQueue {
class SimpleStringQueueManager {
    public:
    SimpleStringQueueManager(AMQP::Address address, std::string queueName);

    void publish(const std::string& message);
    std::optional<std::string> consume();

    private:
    AmqpQueueHandler _queueHandler;
    std::list<std::string> _receivedMessage{};
};

} // namespace MessageQueue