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