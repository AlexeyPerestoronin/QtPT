#include <MessageQueue/SimpleStringQueueManager.hpp>

#include <amqpcpp/address.h>
#include <gtest/gtest.h>
#include <memory>

TEST(PublishAndConsume, publish_two_values) {
    auto StringQueueManager = std::make_unique<SimpleStringQueueManager>(AMQP::Address{"amqp://guest:guest@localhost/"}, "test_queue");

    ASSERT_NO_THROW(StringQueueManager->publish("message one"));
    ASSERT_NO_THROW(StringQueueManager->publish("message two"));

    std::this_thread::sleep_for(std::chrono::seconds(1));
    ASSERT_TRUE(StringQueueManager->consume().has_value());
    ASSERT_TRUE(StringQueueManager->consume().has_value());
}