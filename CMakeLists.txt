cmake_minimum_required(VERSION 3.15)

project(LeetCode
    VERSION 1.0
    DESCRIPTION "LeetCode's problem solving project")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include("$ENV{LEET_CODE_DIR}/cmake/AddSuitTests.cmake")
AddSuitTests("$ENV{LEET_CODE_DIR}/src/Easy")
AddSuitTests("$ENV{LEET_CODE_DIR}/src/Medium")
AddSuitTests("$ENV{LEET_CODE_DIR}/src/ Hard")
