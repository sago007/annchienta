# CMakeLists.txt for annchienta/src

# Also compile subdirectory.
ADD_SUBDIRECTORY( xml )

# Generate python swig file through:
ADD_CUSTOM_TARGET(
     swig
     swig -python -c++ -o ${ANNCHIENTA_BINARY_DIR}/src/annchienta_wrap.cpp -outdir ${ANNCHIENTA_BINARY_DIR}/modules ${ANNCHIENTA_BINARY_DIR}/src/annchienta_interface.i
)

# Set up include directories.
INCLUDE_DIRECTORIES(
    ${SDL_INCLUDE_DIR}
    ${SDLMIXER_INCLUDE_DIR}
    ${PYTHON_INCLUDE_PATH}
    ${PNG_INLUDE_DIR}
    ${OPENGL_INCLUDE_DIR}
    ${FREETYPE_INCLUDE_DIRS}
)

ADD_LIBRARY( 
    annchienta SHARED annchienta_wrap.cpp 
    Area.cpp AudioManager.cpp CacheManager.cpp Engine.cpp Entity.cpp Font.cpp InputManager.cpp InputPersonControl.cpp Layer.cpp LogManager.cpp Map.cpp MapManager.cpp Mask.cpp MathManager.cpp PersonControl.cpp Person.cpp Point.cpp SamplePersonControl.cpp Sound.cpp StaticObject.cpp Surface.cpp Tile.cpp TileSet.cpp Vector.cpp VideoManager.cpp
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

# Right name for annchienta so we can import it.
SET_TARGET_PROPERTIES( annchienta PROPERTIES PREFIX "_" )

# Put annchienta in the right location.
INSTALL(
    TARGETS annchienta
    DESTINATION ${PYTHON_SITE_PACKAGES}
)
