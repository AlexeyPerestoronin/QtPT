include("$ENV{LEET_CODE_DIR}/cmake/FindAllSourceFiles.cmake")

find_package(GTest REQUIRED)

# brief: creates suit tests
# param: i_targetTestFile - target file for new suit-test
function(AddSuitTest i_targetTestFile)
    message("[add suit-test: ${i_targetTestFile}] begin")

    get_filename_component(fileNameWithoutExtension ${i_targetTestFile} NAME_WE)
    set(suitTestExeName ${fileNameWithoutExtension})
    add_executable(${suitTestExeName}
        "$ENV{LEET_CODE_DIR}/src/main.cpp"
        ${i_targetTestFile})
    target_include_directories(${suitTestExeName}
        PRIVATE
        "$ENV{LEET_CODE_DIR}/src"
        # GTest
        ${gtest_SOURCE_DIR}/include
        ${gmock_SOURCE_DIR}/include)
    target_link_libraries(${suitTestExeName} PRIVATE gtest::gtest)
    # target_link_libraries(${suitTestExeName} GTest::gtest_main)
    # target_link_libraries(${suitTestExeName} GTest::gmock_main)

    message("[add suit-test: ${i_targetTestFile}] end")
endfunction(AddSuitTest)


# brief: creates suit tests
# note1: one suit test is creates from one code file and presents as unique project
# param: i_testsSource - name of dirrectory with tests
function(AddSuitTests i_testsSource)
    message("[AddSuitTests] begin")

    file(GLOB_RECURSE sources_list "${i_testsSource}/*")
    foreach(source ${sources_list})
        if(NOT IS_DIRECTORY ${source})
            get_filename_component(sourceExt ${source} EXT)
            if(${sourceExt} STREQUAL ".cpp")
                AddSuitTest(${source})
            endif()
        endif()
    endforeach()

    message("[AddSuitTests] end")
endfunction(AddSuitTests)
