#include <MessageQueue/AmqpQueueHandler.hpp>

#include <fmt/format.h>

#include <stdexcept>
#include <string>
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
            })
        .onError(
            [](const char* message)
            {
                throw std::runtime_error(fmt::format("queue declaration error: {}", message));
            });

    _chanel.consume(_queueName)
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
}

AmqpQueueHandler::~AmqpQueueHandler() {
    event_base_free(_eventBase);
}

void AmqpQueueHandler::publish(const std::string_view& exchange, const std::string_view& message) {
    _chanel.publish(exchange, _queueName, message, 0);
}