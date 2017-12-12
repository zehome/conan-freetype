project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory(sources)

set(DEST_DIR "${CMAKE_INSTALL_PREFIX}")
CONFIGURE_FILE("freetype.pc.in" "freetype.pc" @ONLY)
CONFIGURE_FILE("freetype.pc.in" "freetype2.pc" @ONLY)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/freetype.pc" DESTINATION lib/pkgconfig)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/freetype2.pc" DESTINATION lib/pkgconfig)
