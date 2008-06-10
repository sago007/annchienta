# CMakeLists.txt for annchienta/src

ADD_SUBDIRECTORY( xml )

# Generate python file through:
ADD_CUSTOM_TARGET(
     swig
     swig -python -c++ -o ${ANNCHIENTA_BINARY_DIR}/src/annchienta_wrap.cpp -outdir ${ANNCHIENTA_BINARY_DIR}/modules ${ANNCHIENTA_BINARY_DIR}/src/annchienta_interface.i
)

# Find our needed Packages.
# FIND_PACKAGE(PythonLibs REQUIRED)
# FIND_PACKAGE(SDL REQUIRED)
# FIND_PACKAGE(SDL_mixer REQUIRED)
# FIND_PACKAGE(Freetype REQUIRED)
# FIND_PACKAGE(PNG REQUIRED)
# FIND_PACKAGE(OpenGL REQUIRED)

#pkg_check_modules(FT2 freetype2)

# Set up include directories.
INCLUDE_DIRECTORIES(
    ${SDL_INCLUDE_DIR}
    ${SDLMIXER_INCLUDE_DIR}
    ${PYTHON_INCLUDE_PATH}
    ${PNG_INLUDE_DIR}
    ${OPENGL_INCLUDE_DIR}
    ${FREETYPE_INCLUDE_DIRS}
)

ADD_EXECUTABLE(
    annchienta annchienta_wrap.cpp area.cpp audiomanager.cpp auxfunc.cpp cachemanager.cpp engine.cpp entity.cpp font.cpp inputmanager.cpp inputpersoncontrol.cpp layer.cpp logmanager.cpp main.cpp map.cpp mapmanager.cpp mask.cpp personcontrol.cpp person.cpp point.cpp samplepersoncontrol.cpp sound.cpp staticobject.cpp surface.cpp tile.cpp tileset.cpp videomanager.cpp
)

# Link to the following libraries
TARGET_LINK_LIBRARIES(
    annchienta
    irrXML
    ${SDL_LIBRARY}
    ${SDLMIXER_LIBRARY}
    ${PYTHON_LIBRARIES}
    ${PNG_LIBRARIES}
    ${OPENGL_LIBRARIES}
    ${FREETYPE_LIBRARIES}

    # Needed for python, ld errors without it.
    util
)

# Put annchienta in the right location.
INSTALL(
    TARGETS annchienta
    DESTINATION bin
)
