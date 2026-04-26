#pragma once

#include <amqpcpp.h>
#include <amqpcpp/libevent.h>

class AmqpQueueManager {
    public:
    AmqpQueueManager(AMQP::Address address, std::string queue_name);

    void publish(const std::string& message) const;

    private:
    AMQP::LibEventHandler _handler;
    AMQP::TcpConnection _connection;
    AMQP::TcpChannel _chanel;
};