#include <MessageQueue/AmqpQueueHandler.hpp>

#include <event2/event.h>
#include <fmt/base.h>
#include <fmt/format.h>

#include <stdexcept>
#include <string>
#include <thread>
#include <utility>

AmqpQueueHandler::AmqpQueueHandler(AMQP::Address address, std::string queueName, ConsumeCallbackHandler consumeCallback)
    : _eventBase{event_base_new()}
    , _handler{_eventBase}
    , _connection{&_handler, std::move(address)}
    , _chanel{&_connection}
    , _queueName{std::move(queueName)}
    , _consumeCallback{std::move(consumeCallback)} {

    _chanel.declareQueue(_queueName)
        .onSuccess(
            [this]()
            {
                fmt::println("'{}'-queue successfully connected", _queueName);
            })
        .onError(
            [this](const char* message)
            {
                throw std::runtime_error(fmt::format("'{}'-queue declaration error: {}", _queueName, message));
            });

    _chanel.consume(_queueName, AMQP::noack)
        .onReceived(
            [&](const AMQP::Message& message, uint64_t deliveryTag, bool redelivered)
            {
                _consumeCallback(std::string(message.body(), message.bodySize()));
            })
        .onError(
            [this](const char* message)
            {
                throw std::runtime_error(fmt::format("consume error on ''-queue: {}", _queueName, message));
            });

    _dispatchThreadOpt = std::thread(
        [this]()
        {
            fmt::println("event dispatch for '{}'-queue is started...", _queueName);
            event_base_dispatch(_eventBase);
        });
}

AmqpQueueHandler::~AmqpQueueHandler() {
    fmt::println("event dispatch for '{}'-queue is stoping...", _queueName);
    if (_dispatchThreadOpt && _dispatchThreadOpt->joinable()) {
        event_base_loopbreak(_eventBase);
        _dispatchThreadOpt->join();
    }
    fmt::println("event dispatch for '{}'-queue is stoped", _queueName);

    if (_eventBase) {
        event_base_free(_eventBase);
    }
    fmt::println("free resourced for for '{}'-queue", _queueName);
}

void AmqpQueueHandler::publish(const std::string_view& exchange, const std::string_view& message) {
    _chanel.publish(exchange, _queueName, message, 0);
}