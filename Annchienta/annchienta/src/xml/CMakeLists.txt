# CMakeLists.txt for annchienta/src/xml

# After a compile problem found by Patrick Horn
IF( CMAKE_COMPILER_IS_GNUCXX )
    SET( CMAKE_CXX_FLAGS "-fPIC" )
ENDIF( CMAKE_COMPILER_IS_GNUCXX )

# Add our XML library.
ADD_LIBRARY(
    irrXML STATIC irrXML.cpp
)
