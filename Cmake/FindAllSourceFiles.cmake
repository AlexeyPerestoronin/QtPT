# brief: finds all files recursively which must be using as target compiler files
# param: i_prescription - some prescription about what is this function do
# param: i_whichDirectory - first directory for to start recursively viewing
# param: i_listIgnoredDirrectory - list of directories are impossible to use files from
# param: i_listAvalibleFilesTemplates - list of files-names templates using to determ available source files
# param: o_result - result list with files
function(FindAllSourceFiles i_prescription i_whichDirectory i_listIgnoredDirrectory i_listAvalibleFilesTemplates o_result)
    message("[${i_prescription}] begin")

    file(GLOB_RECURSE items "${i_whichDirectory}/*")
    
    set(listPossibilityFiles "")
    foreach(item ${items})
        if(IS_DIRECTORY ${item})
            continue()
        endif()
        foreach(availableFileTemplate ${i_listAvalibleFilesTemplates})
            if("${item}" MATCHES "^${i_whichDirectory}/.*${availableFileTemplate}$")
                list(APPEND listPossibilityFiles ${item})
            endif()
        endforeach()
    endforeach()

    set(listTargetSourceFiles "")
    foreach(possibleFile ${listPossibilityFiles})
        set(isOneRestrictedItem "false")
        get_filename_component(filePath ${possibleFile} PATH)
        foreach(ignoredDir ${i_listIgnoredDirrectory})
            if(${filePath} MATCHES "^${ignoredDir}.*")
                set(isOneRestrictedItem "true")
                break()
            endif()
        endforeach()
        if("${isOneRestrictedItem}" MATCHES "^false$")
            list(APPEND listTargetSourceFiles ${possibleFile})
            message("\t[PF] ${possibleFile}")
        endif()
    endforeach()

    # set the result value
    set(${o_result} ${listTargetSourceFiles} PARENT_SCOPE)
    message("[${i_prescription}] end")
endfunction(FindAllSourceFiles)
