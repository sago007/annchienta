# CMakeLists.txt for elegiac_convergence

# We need 2.6 because cmake has freetype2 support from then onwards.
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT(ELEGIAC_CONVERGENCE)

# Install all directories to /usr/share/annchienta/elegiac_convergence
INSTALL(
    DIRECTORY assets images locations masks music saves scripts sounds sprites tiles
    DESTINATION share/annchienta/elegiac_convergence
    # We don't want any svn shit installed.
    PATTERN ".svn" EXCLUDE
)

# We determine what the write directory is, based on the OS.
IF(WIN32)
    SET(WRITEDIR ".annchienta")
ELSE(WIN32)
    SET(WRITEDIR "~/.annchienta")
ENDIF(WIN32)

# We create a small startup script that will launch elegiac_convergence
FILE(
    WRITE elegiac-convergence
    "mkdir -p ${WRITEDIR}\n"
    "annchienta ${CMAKE_INSTALL_PREFIX}/share/annchienta/elegiac_convergence/scripts/main.py ${CMAKE_INSTALL_PREFIX}/share/annchienta/modules ${WRITEDIR}\n"
)

# Install that script. Use programs instead of files for chmod +x
INSTALL(
    PROGRAMS elegiac-convergence
    DESTINATION bin
)

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
