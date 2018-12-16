project(cmake_wrapper)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(conanbuildinfo.cmake)
conan_basic_setup()


add_definitions("-DHB_SCRIPT_ADLAM=1097100397")
add_definitions("-DHB_SCRIPT_OSAGE=1332963173")

add_subdirectory(source_subfolder)

set(DEST_DIR "${CMAKE_INSTALL_PREFIX}")
CONFIGURE_FILE("freetype.pc.in" "freetype.pc" @ONLY)
CONFIGURE_FILE("freetype.pc.in" "freetype2.pc" @ONLY)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/freetype.pc" DESTINATION lib/pkgconfig)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/freetype2.pc" DESTINATION lib/pkgconfig)
