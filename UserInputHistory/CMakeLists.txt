cmake_minimum_required(VERSION 3.15)

project(UserInputHistory
    VERSION 1.0
    DESCRIPTION "Qt project template")

set(CMAKE_CXX_COMPILER clang++)
set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Qt variables for processing Q_OBJECT and forms
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)
find_package(Qt6 REQUIRED CONFIG COMPONENTS Widgets)


include("$ENV{PROJECT_GIT_DIR}/Cmake/FindAllSourceFiles.cmake")
FindAllSourceFiles(
    ROOT_DIR $ENV{USER_INPUT_HISTORY_DIR}/src
    FILE_TYPES "**.cpp" "**.hpp"
    RESULT UIH_SOURCES_FILES
)


add_executable(UserInputHistory ${UIH_SOURCES_FILES})
target_link_libraries(UserInputHistory PRIVATE Qt6::Widgets)