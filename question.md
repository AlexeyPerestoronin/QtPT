Смотри, я сделал вот такую реализацию:

MessageQueue/src/AmqpQueueHandler.cpp
```cpp
#pragma once

#include <amqpcpp.h>
#include <amqpcpp/libevent.h>

#include <optional>
#include <string>
#include <string_view>
#include <thread>

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
```

MessageQueue/src/AmqpQueueHandler.cpp
```cpp
#include <MessageQueue/AmqpQueueHandler.hpp>

#include <event2/event.h>
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

    _dispatchThreadOpt = std::thread(
        [this]()
        {
            event_base_dispatch(_eventBase);
        });
}

AmqpQueueHandler::~AmqpQueueHandler() {
    event_base_loopbreak(_eventBase);
    _dispatchThreadOpt.value().join();
    event_base_free(_eventBase);
}

void AmqpQueueHandler::publish(const std::string_view& exchange, const std::string_view& message) {
    _chanel.publish(exchange, _queueName, message, 0);
}
```

MessageQueue/include/MessageQueue/SimpleStringQueueManager.hpp
```cpp
#pragma once

#include "AmqpQueueHandler.hpp"

#include <list>
#include <optional>

class SimpleStringQueueManager {
    public:
    SimpleStringQueueManager(AMQP::Address address, std::string queueName);

    void publish(const std::string& message);
    std::optional<std::string> consume();

    private:
    AmqpQueueHandler _queueHandler;
    std::list<std::string> _receivedMessage{};
};
```

MessageQueue/src/SimpleStringQueueManager.cpp
```
#include <MessageQueue/SimpleStringQueueManager.hpp>

SimpleStringQueueManager::SimpleStringQueueManager(AMQP::Address address, std::string queueName)
    : _queueHandler{std::move(address),
                    std::move(queueName),
                    [&](std::string message)
                    {
                        this->_receivedMessage.push_back(std::move(message));
                    }} {
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
```

А так же unit-тесты, которые проверяют работоспособность данного решения:
```cpp
#include <MessageQueue/SimpleStringQueueManager.hpp>

#include <amqpcpp/address.h>
#include <gtest/gtest.h>
#include <memory>

auto StringQueueManager = std::make_unique<SimpleStringQueueManager>(AMQP::Address{"amqp://guest:guest@localhost/"}, "test_queue");

TEST(PublishAndConsume, publish_two_values) {
    ASSERT_NO_THROW(StringQueueManager->publish("message one"));
    ASSERT_NO_THROW(StringQueueManager->publish("message two"));
}

TEST(PublishAndConsume, consume_1st_value) {
    ASSERT_EQ(StringQueueManager->consume().value_or("nothing"), "message one");
}

TEST(PublishAndConsume, consume_2nd_value) {
    ASSERT_EQ(StringQueueManager->consume().value_or("nothing"), "message two");
}
```

Проблема в том, что первые тест проходит успешно, что, вроде, говорит о том, что сообщения отправлены, однако два последующих теста завершаются ошибкой: сообщения в очереди нет.
Что не так с моим кодом?