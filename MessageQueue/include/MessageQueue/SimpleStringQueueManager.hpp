#pragma once

#include <amqpcpp.h>
#include <amqpcpp/libevent.h>

#include <list>
#include <optional>
#include <string>
#include <string_view>

using ConsumeCallbackHandler = std::function<void(const std::string&)>;

class SimpleStringQueueManager {
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
    };

    public:
    SimpleStringQueueManager(AMQP::Address address, std::string queueName);

    void publish(const std::string& message);
    std::optional<std::string> consume();

    private:
    AmqpQueueHandler _queueHandler;
    std::list<std::string> _receivedMessage{};
};