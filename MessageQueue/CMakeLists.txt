cmake_minimum_required(VERSION 3.15)
project(MessageQueue
    VERSION 1.0
    DESCRIPTION "RabbitMQ based local message queue")

include("$ENV{PROJECT_GIT_DIR}/Cmake/CompilerSettings.cmake")
include("$ENV{PROJECT_GIT_DIR}/Cmake/FindAllSourceFiles.cmake")

find_package(amqpcpp REQUIRED)

FindAllSourceFiles(
    ROOT_DIR $ENV{MESSAGE_QUEUE_DIR}/src
    FILE_TYPES "**.cpp" "**.hpp"
    RESULT CPP_MQ_SOURCES_FILES
)

add_library(MessageQueue SHARED ${CPP_MQ_SOURCES_FILES})

target_link_libraries(MessageQueue PRIVATE amqpcpp)
