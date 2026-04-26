cmake_minimum_required(VERSION 3.15)
project(MessageQueue
    VERSION 1.0
    DESCRIPTION "RabbitMQ based local message queue")

include("$ENV{PROJECT_GIT_DIR}/Cmake/CompilerSettings.cmake")
include("$ENV{PROJECT_GIT_DIR}/Cmake/FindAllSourceFiles.cmake")

find_package(amqpcpp REQUIRED)
find_package(Libevent REQUIRED)
find_package(OpenSSL REQUIRED)

FindAllSourceFiles(
    ROOT_DIR $ENV{MESSAGE_QUEUE_DIR}/src
    FILE_TYPES "**.cpp" "**.hpp"
    RESULT CPP_MQ_SOURCES_FILES
)

add_library(MessageQueue SHARED ${CPP_MQ_SOURCES_FILES})

target_link_libraries(MessageQueue
    PRIVATE
        openssl::openssl
        libevent::libevent
        amqpcpp
)

target_include_directories(MessageQueue
    PUBLIC
        $ENV{MESSAGE_QUEUE_DIR}/include
    PRIVATE 
        $ENV{MESSAGE_QUEUE_DIR}/src
)

# add tests
find_package(GTest REQUIRED)

FindAllSourceFiles(
    ROOT_DIR $ENV{MESSAGE_QUEUE_DIR}/tests/unit
    FILE_TYPES "**.cpp"
    RESULT CPP_MQT_SOURCES_FILES
)

add_executable(MessageQueueTests tests/test_main.cpp ${CPP_MQT_SOURCES_FILES})

target_link_libraries(MessageQueueTests
    PRIVATE
        gtest::gtest
        GTest::gtest_main
        MessageQueue
)
