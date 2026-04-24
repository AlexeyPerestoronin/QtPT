cmake_minimum_required(VERSION 3.15)

project(LeetCode
    VERSION 1.0
    DESCRIPTION "QtPT")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include("$ENV{PROJECT_GIT_DIR}/Cmake/FindAllSourceFiles.cmake")
FindAllSourceFiles(
    ROOT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src"
    IGNORED_SUBDIR_LIST 
        "${CMAKE_CURRENT_SOURCE_DIR}/src/third_party"
        "${CMAKE_CURRENT_SOURCE_DIR}/src/tests/data"
    FILE_TYPES "*.cpp" "*.hpp"
    RESULT MY_SOURCES
)