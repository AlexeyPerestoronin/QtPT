#pragma once

#include <amqpcpp.h>
#include <amqpcpp/libevent.h>

#include <optional>
#include <string>
#include <string_view>
#include <thread>

namespace MessageQueue {

using ConsumeCallbackHandler = std::function<void(std::string)>;

class AmqpQueueHandler {
    public:
    AmqpQueueHandler(AMQP::Address address, std::string queueName, ConsumeCallbackHandler consumeCallback);
    ~AmqpQueueHandler();

    void publish(const std::string_view& exchange, const std::string_view& message);

    private:
    event_base* _eventBase;
    AMQP::LibEventHandler _handler;
    AMQP::TcpConnection _connection;
    AMQP::TcpChannel _chanel;
    std::string _queueName;
    ConsumeCallbackHandler _consumeCallback;
    std::optional<std::thread> _dispatchThreadOpt{};
};

} // namespace MessageQueue