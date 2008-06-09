# CMakeLists.txt for annchienta

# We need 2.6 because cmake has freetype2 support from then onwards.
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)


PROJECT(ANNCHIENTA)

SET( ANNCHIENTA_ROOT ${ANNCHIENTA_BINARY_DIR})

ADD_SUBDIRECTORY(src)

# For the uninstall rule.
CONFIGURE_FILE(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake_uninstall.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
    IMMEDIATE @ONLY
)

# For the uninstall rule.
ADD_CUSTOM_TARGET(
    uninstall
    "${CMAKE_COMMAND}" -P "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
)