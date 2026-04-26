#include <MessageQueue/SimpleStringQueueManager.hpp>

#include <optional>
#include <string>
#include <utility>

SimpleStringQueueManager::AmqpQueueHandler::AmqpQueueHandler(AMQP::Address address, std::string queueName, ConsumeCallbackHandler consumeCallback)
    : _eventBase{event_base_new()}
    , _handler{_eventBase}
    , _connection{&_handler, std::move(address)}
    , _chanel{&_connection}
    , _queueName{std::move(queueName)}
    , _consumeCallback{std::move(consumeCallback)} {

    _chanel.declareQueue(_queueName)
        .onSuccess([this]() { std::cout << "Successfully declared queue: " << _queueName << std::endl; })
        .onError([](const char* message) { std::cerr << "Queue declaration error: " << message << std::endl; });

    _chanel.consume(_queueName)
        .onReceived([&](const AMQP::Message& message, uint64_t deliveryTag, bool redelivered) {
            std::string body(message.body(), message.bodySize());
            _consumeCallback(body);
        })
        .onError([this](const char* message) { std::cerr << "Consume error on queue " << _queueName << ": " << message << std::endl; });
}

SimpleStringQueueManager::AmqpQueueHandler::~AmqpQueueHandler() {
    event_base_free(_eventBase);
}

void SimpleStringQueueManager::AmqpQueueHandler::publish(const std::string_view& exchange, const std::string_view& message) {
    _chanel.publish(exchange, _queueName, message, 0);
}

SimpleStringQueueManager::SimpleStringQueueManager(AMQP::Address address, std::string queueName)
    : _queueHandler{std::move(address), std::move(queueName), [&](std::string message) { this->_receivedMessage.push_back(std::move(message)); }} {
}

void SimpleStringQueueManager::publish(const std::string& message) {
    std::string defaultExchange{""};
    _queueHandler.publish(defaultExchange, message);
}

std::optional<std::string> SimpleStringQueueManager::consume() {
    if (!_receivedMessage.empty()) {
        auto message = _receivedMessage.front();
        _receivedMessage.pop_front();
        return message;
    }

    return std::nullopt;
}