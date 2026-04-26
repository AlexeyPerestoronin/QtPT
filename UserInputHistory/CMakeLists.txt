cmake_minimum_required(VERSION 3.15)
project(UserInputHistory
    VERSION 1.0
    DESCRIPTION "Qt project template")

include("$ENV{PROJECT_GIT_DIR}/Cmake/CompilerSettings.cmake")
include("$ENV{PROJECT_GIT_DIR}/Cmake/FindAllSourceFiles.cmake")

# Qt variables for processing Q_OBJECT and forms
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED CONFIG COMPONENTS Qml Quick Core)

FindAllSourceFiles(
    ROOT_DIR $ENV{USER_INPUT_HISTORY_DIR}/src
    FILE_TYPES "**.cpp" "**.hpp"
    RESULT CPP_UIH_SOURCES_FILES
)

add_executable(UserInputHistory ${CPP_UIH_SOURCES_FILES} ${RESOURCES})

target_link_libraries(UserInputHistory
    PRIVATE
        Qt6::Qml
        Qt6::Quick
        Qt6::Core)

qt_add_qml_module(UserInputHistory
    URI App
    VERSION 1.0
    QML_FILES qml/main.qml
)
