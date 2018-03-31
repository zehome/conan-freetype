project(test_package C)
cmake_minimum_required(VERSION 2.8.11)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(Freetype 2.8.1 REQUIRED)

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/OpenSans-Bold.ttf
     DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

file(GLOB SOURCE_FILES *.c)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
