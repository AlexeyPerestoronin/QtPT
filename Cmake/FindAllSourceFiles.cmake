include(CMakeParseArguments)

function(FindAllSourceFiles)
    set(options "")
    set(oneValueArgs ROOT_DIR RESULT)
    set(multiValueArgs IGNORED_SUBDIR_LIST FILE_TYPES)
    cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ALGN})

    message(STATUS "--- Scanning: ${ARG_ROOT_DIR} ---")

    # prepare templates for searching
    set(globTemplates "")
    foreach(ext ${ARG_FILE_TYPES})
        list(APPEND globTemplates "${ARG_ROOT_DIR}/${ext}")
    endforeach()

    # recursive search
    file(GLOB_RECURSE allFiles LIST_DIRECTORIES false ${globTemplates})

    set(filteredList "")

    foreach(filePath ${allFiles})
        set(isIgnored FALSE)
        
        # filtering ignored directory
        foreach(ignoredDir ${ARG_IGNORED_SUBDIR_LIST})
            if(filePath MATCHES "^${ignoredDir}")
                set(isIgnored TRUE)
                break()
            endif()
        endforeach()

        if(NOT isIgnored)
            list(APPEND filteredList "${filePath}")
            message(STATUS "+ ${filePath}")
        endif()
    endforeach()

    # set returning result
    set(${ARG_RESULT} "${filteredList}" PARENT_SCOPE)
endfunction()
