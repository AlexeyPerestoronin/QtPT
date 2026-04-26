// #pragma once

// #include <amqpcpp/address.h>
// #include <amqpcpp/libevent.h>
// #include <amqpcpp/linux_tcp/tcpchannel.h>
// #include <amqpcpp/linux_tcp/tcpconnection.h>

// #include <string>

// class AmqpQueueManager {
//     public:
//     AmqpQueueManager(AMQP::Address address, std::string queue_name);

//     void publish(const std::string& message) const;

//     private:
//     AMQP::LibEventHandler _handler;
//     AMQP::TcpConnection _connection;
//     AMQP::TcpChannel _chanel;
// };