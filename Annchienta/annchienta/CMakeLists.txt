# CMakeLists.txt for annchienta

##########################
# GENERAL OPTIONS
##########################
# We need 2.6 because cmake has freetype2 support from then onwards.
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT(ANNCHIENTA)

##########################
# SDL
##########################
FIND_PACKAGE(SDL)
IF(SDL_FOUND)
    MESSAGE( STATUS "SDL has been found:" )
    MESSAGE( STATUS "\tCFLAGS : ${SDL_INCLUDE_DIR}" )
    MESSAGE( STATUS "\tLDFLAGS: ${SDL_LIBRARY}" )
ELSE(SDL_FOUND)
    SET( SDL_INCLUDE_DIR NOTFOUND )
    SET( SDL_LIBRARY NOTFOUND )
    MESSAGE( STATUS "SDL is required")
ENDIF(SDL_FOUND)

##########################
# SDL_mixer
##########################
FIND_PACKAGE(SDL_mixer)
IF( SDLMIXER_FOUND )
    # take a lucky guess
    IF(${SDLMIXER_INCLUDE_DIR} MATCHES "NOTFOUND")
        SET(SDLMIXER_INCLUDE_DIR ${SDL_INCLUDE_DIR})
    ENDIF(${SDLMIXER_INCLUDE_DIR} MATCHES "NOTFOUND")
        MESSAGE( STATUS "SDL_mixer has been found:" )
        MESSAGE( STATUS "\tCFLAGS : ${SDLMIXER_INCLUDE_DIR}" )
        MESSAGE( STATUS "\tLDFLAGS: ${SDLMIXER_LIBRARY}" )
ELSE( SDLMIXER_FOUND )
    SET( SDLMIXER_INCLUDE_DIR NOTFOUND )
    SET( SDLMIXER_LIBRARY NOTFOUND )
    MESSAGE( STATUS "SDL_mixer is required" )
ENDIF(SDLMIXER_FOUND)

#######################
# Python
#######################
FIND_PACKAGE(PythonLibs)
IF(PYTHON_INCLUDE_PATH)
    MESSAGE( STATUS "Python has been found:" )
    MESSAGE( STATUS "\tCFLAGS : ${PYTHON_INCLUDE_PATH}" )
    MESSAGE( STATUS "\tLDFLAGS: ${PYTHON_LIBRARIES}" )
ELSE(PYTHON_INCLUDE_PATH)
    SET( PYTHON_INCLUDE_PATH NOTFOUND )
    SET( PYTHON_LIBRARIES NOTFOUND )
    MESSAGE( STATUS "A Python installation is required" )
ENDIF(PYTHON_INCLUDE_PATH)

FIND_PACKAGE(PythonInterp)
IF(PYTHONINTERP_FOUND)
	EXEC_PROGRAM( ${PYTHON_EXECUTABLE}
                  ARGS "-c \"import sys;vi = sys.version_info; print \\\"python%s.%s\\\" %(vi[0],vi[1])\""
                  OUTPUT_VARIABLE PYTHON_VERSION_DIR	
	)
	SET( PYTHON_SITE_PACKAGES "lib/${PYTHON_VERSION_DIR}/site-packages" )
	MESSAGE( STATUS	"\tVERSION: ${PYTHON_VERSION_DIR}" )
	MESSAGE( STATUS "\tInstalling modules to: ${PYTHON_SITE_PACKAGES}" )
ELSE(PYTHONINTERP_FOUND)
	MESSAGE( STATUS	"Impossible to find the Python Interpreter" )
ENDIF(PYTHONINTERP_FOUND)

#######################
# libZ
#######################
FIND_PACKAGE(ZLIB)

#######################
# PNG
#######################
FIND_PACKAGE(PNG)
if(PNG_FOUND)
    MESSAGE( STATUS "PNG has been found:" )
    MESSAGE( STATUS "\tCFLAGS : ${PNG_INCLUDE_DIR}" )
    MESSAGE( STATUS "\tLDFLAGS: ${PNG_LIBRARY}" )
else(PNG_FOUND)
    SET( PNG_INCLUDE_DIR NOTFOUND )
    SET( PNG_LIBRARY NOTFOUND )
    MESSAGE( STATUS "PNG is required" )
endif(PNG_FOUND)

#######################
# OpenGL
#######################
FIND_PACKAGE(OpenGL)
IF(OPENGL_INCLUDE_DIR)
    MESSAGE( STATUS "OpenGL has been found:" )
    MESSAGE( STATUS "\tCFLAGS : ${OPENGL_INCLUDE_DIR}" )
    MESSAGE( STATUS "\tLDFLAGS: ${OPENGL_LIBRARY}" )
ELSE(OPENGL_INCLUDE_DIR)
    SET( OPENGL_INCLUDE_DIR NOTFOUND )
    SET( OPENGL_LIBRARY NOTFOUND )
    MESSAGE( STATUS "OpenGL is required" )
ENDIF(OPENGL_INCLUDE_DIR)

#######################
# Freetype
#######################
FIND_PACKAGE(Freetype)
IF(FREETYPE_INCLUDE_DIRS)
    MESSAGE( STATUS "Freetype has been found:" )
    MESSAGE( STATUS "\tCFLAGS : ${FREETYPE_INCLUDE_DIRS}" )
    MESSAGE( STATUS "\tLDFLAGS: ${FREETYPE_LIBRARIES}" )
ELSE(FREETYPE_INCLUDE_DIRS)
    SET( FREETYPE_INCLUDE_DIRS NOTFOUND )
    SET( FREETYPE_LIBRARIES NOTFOUND )
    MESSAGE( STATUS "Freetype is required" )
ENDIF(FREETYPE_INCLUDE_DIRS)

# Continue.
ADD_SUBDIRECTORY(src)
ADD_SUBDIRECTORY(doc)

# Install modules to the right place.
INSTALL(
    FILES modules/annchienta.py
    DESTINATION ${PYTHON_SITE_PACKAGES}
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

