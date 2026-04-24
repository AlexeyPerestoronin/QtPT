cmake_minimum_required(VERSION 3.15)

project(UserInputHistory
    VERSION 1.0
    DESCRIPTION "Qt project template")

set(CMAKE_CXX_COMPILER clang)
set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include("$ENV{PROJECT_GIT_DIR}/Cmake/FindAllSourceFiles.cmake")
FindAllSourceFiles(
    ROOT_DIR $ENV{USER_INPUT_HISTORY_DIR}/src
    FILE_TYPES "**.cpp" "**.hpp"
    RESULT UIH_SOURCES_FILES
)