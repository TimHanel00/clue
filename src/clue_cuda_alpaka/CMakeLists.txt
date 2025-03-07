# mainAlpakaCUDA: this will build the native C++ implementation of CLUE and its
#       corresponding CUDA one built using ALPAKA. Which one to use must be
#       selected at runtime via a flag.

#if(CMAKE_CUDA_COMPILER)
  #set_source_files_properties(${PROJECT_SOURCE_DIR}/src/main.cpp PROPERTIES LANGUAGE CUDA)
  alpaka_add_executable(mainAlpakaCUDA ${PROJECT_SOURCE_DIR}/src/main.cpp)
  target_compile_definitions(mainAlpakaCUDA PRIVATE USE_ALPAKA)
  target_compile_options(mainAlpakaCUDA PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:
                        -Xcompiler;
                        -m64;
                        -expt-relaxed-constexpr;
                        -w;
  >
  )
  target_link_libraries(mainAlpakaCUDA PRIVATE CLUELib)
  target_link_libraries(mainAlpakaCUDA PRIVATE alpaka::alpaka)

  target_include_directories(mainAlpakaCUDA PUBLIC
    $<BUILD_INTERFACE:${ALPAKA_DIR}/include>
    PUBLIC
    $<BUILD_INTERFACE:${ALPAKA_DIR}/alpaka/include>
    PUBLIC
    $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  )
#endif(CMAKE_CUDA_COMPILER)
