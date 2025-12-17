cmake_minimum_required(VERSION 3.8)

project(
  CLUE
  VERSION 1.1.0
  DESCRIPTION "The CLUstering by Energy algorithm"
  LANGUAGES CXX)

# Location of the ALPAKA
set(ALPAKA_DIR ${CMAKE_CURRENT_SOURCE_DIR}/alpaka CACHE PATH "Path to ALPAKA (by default: submodule)")

# Activate VERBOSE output
set(CMAKE_VERBOSE_MAKEFILE OFF)

# Check for CUDA
include(CheckLanguage)
check_language(CUDA)
if(CMAKE_CUDA_COMPILER)
  enable_language(CUDA)
  set(CMAKE_CXX_STANDARD 20)
  if(NOT CMAKE_CUDA_ARCHITECTURES)
    set(CMAKE_CUDA_ARCHITECTURES "60;70;75;80")
  endif()
else()
  message(STATUS "No CUDA compiler found. Still, you can run the C++ version and alpaka!")
endif()

if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set (CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}/install" CACHE PATH "default install path" FORCE )
endif()

include(GNUInstallDirs)

# Set up C++ Standard
set(CMAKE_CXX_STANDARD 20 CACHE STRING "")

if(NOT CMAKE_CXX_STANDARD MATCHES "17|20")
  message(FATAL_ERROR "Unsupported C++ standard: ${CMAKE_CXX_STANDARD}")
endif()

add_subdirectory("${CMAKE_CURRENT_LIST_DIR}/alpaka")

add_subdirectory(clueLib)
add_subdirectory(src)

# SOME TESTS
enable_testing()

function(run_test_cpu target label repeats)
    file(GLOB inputs "${CMAKE_CURRENT_SOURCE_DIR}/data/input/*.csv")
    foreach(input_file IN LISTS inputs)
        get_filename_component(input_name "${input_file}" NAME_WE)
        get_filename_component(input_dir  "${input_file}" DIRECTORY)
        get_filename_component(input_name "${input_file}" NAME_WE)
        get_filename_component(input_ext  "${input_file}" EXT)

        set(test_name   "${input_name}_${label}_CPU")
        set(output_file "${input_dir}/${test_name}${input_ext}")

        add_test(
                NAME "${test_name}"
                COMMAND $<TARGET_FILE:${target}>
                -i "${input_file}"
                -O "${output_file}"
                -d 7.0 -r10.0 -o 2 -e "${repeats}" -v
        )
    endforeach()
endfunction()

function(run_test_gpu target label repeats executor)
    file(GLOB inputs "${CMAKE_CURRENT_SOURCE_DIR}/data/input/*.csv")
    foreach(input_file IN LISTS inputs)

        get_filename_component(input_dir  "${input_file}" DIRECTORY)
        get_filename_component(input_name "${input_file}" NAME_WE)
        get_filename_component(input_ext  "${input_file}" EXT)

        set(test_name   "${input_name}_${label}_${executor}")
        set(output_file "${input_dir}/${test_name}${input_ext}")

        add_test(
                NAME "${test_name}"
                COMMAND $<TARGET_FILE:${target}>
                -i "${input_file}"
                -O "${output_file}"
                -d 7.0 -r10.0 -o 2 -e "${repeats}" -v
                -u "${executor}"
        )
    endforeach()
endfunction()

if(CMAKE_CUDA_COMPILER)
  run_test_cpu(main main 4)
  run_test_cpu(mainAlpaka AlpakaNativeCpu 4)
  run_test_gpu(main CUDA 100 NativeCuda)
endif()

if(alpaka_EXEC_GpuCuda)
  run_test_gpu(mainAlpaka Alpaka 100 GpuCuda)
endif()

if(alpaka_EXEC_CpuOmpBlocks)
  run_test_gpu(mainAlpaka Alpaka 100 CpuOmpBlocks)
endif()


#--- add version files ---------------------------------------------------------
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/CLUEVersion.h
               ${CMAKE_CURRENT_BINARY_DIR}/CLUEVersion.h )
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/CLUEVersion.h
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/CLUE )
include(cmake/CLUECreateConfig.cmake)

install(EXPORT CLUETargets
  NAMESPACE ${PROJECT_NAME}::
  FILE "${PROJECT_NAME}Targets.cmake"
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}/"
  )

message(STATUS "Finished!")
