

TilePoint, IsometricPoint, MapPoint, ScreenPoint = 0,1,2,3

## \brief Holds a Point.
#
#  This class is used for holding Points. You can
#  manipulate the coordinates directly.
#
#  \section point_example1 Example:
#  \code
# import annchienta
# point = annchienta.Point( annchienta.TilePoint, 2, 2 )
# point.x = point.y = point.z = 0
#  \endcode
#
#  Points consist of two or three Coordinates. There are
#  four types of points:
#
#  \section point_types Point Types
#
#  \li TilePoint
#
#  Has X, Y and Z coordinates and refers to a Tile. This
#  means that Point(TilePoint,4,4) would be in the same
#  place as the 4th Tile on the 4th row of Tiles.
#
#  \li IsometricPoint
#
#  Has X, Y and Z coordinates and refers to a Point in
#  an isometric axis system.
#
#  \li MapPoint
#
#  Has X, Y and Z coordinates. Refers to a Point in an ortho
#  axis system. The upper point of the Map translates as
#  (0,0,0). This means negative numbers will occur in the X
#  coordinate.
#
#  \li ScreenPoint
#
#  Has X and Y coordinates and refers to a Point on the
#  screen, where the top-left corner of the game window
#  is (0,0).
#
#  Converting between types is easy, just use the to() and
#  convert() functions.
#
#  \section point_example2 Example:
#  \code
# import annchienta
# videoManager = annchienta.getVideoManager()
# point = annchienta.Point( annchienta.TilePoint, 2, 2 )
# point.convert( ScreenPoint )
# videoManager.drawLine( point.x, point.y, 0, 0 )
#  \endcode
#
#
class Point:

    ## \brief Creates a new Point.
    #
    #  This function creates a new Point with the given
    #  parameters.
    #
    #  \param type Either TilePoint, IsometricPoint, MapPoint or ScreenPoint. See \ref point_types.
    #  \param x Initial X coordinate.
    #  \param y Initial Y coordinate.
    #  \param z Initial Z coordinate.
    #  \return A new Point.
    def __init__( type, x=0, y=0, z=0 ):
        pass

    ## \brief Returns the type of this Point.
    #
    #  \return The type. See \ref point_types.
    def getType():
        pass

    ## \brief Converts to another type.
    #
    #  \param type The new type for this Point. See \ref point_types.
    def convert( type ):
        pass

    ## \brief Creates another type.
    #
    #  \param type The type for the new Point. See \ref point_types.
    #  \return A new Point with the given type.
    def to( type ):
        pass

    ## \brief Checks if this point lies in a rectangle.
    #
    #  \param topLeft Top-left point of the rectangle.
    #  \param bottomRight Bottom-right point of the rectangle.
    #  \return True if this point is enclosed in the rectangle, False if not.
    def isEnclosedBy( topLeft, bottomRight ):
        pass



