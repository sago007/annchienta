
## \brief Holds a Tile.
#
#  This class is used to hold parts of the Layer, called tiles.
#  Because we are using an isometric system, tiles are usually
#  shaped like a rhombus.
#
class Tile(Entity):

    ## \brief Updates this Tile.
    #
    #  This function recompiles the display list for this
    #  Tile. In other words, call this function after you
    #  performed changes to this Tile.
    def makeList():
        pass

    ## \brief Checks for collision with a Point.
    #
    #  \param point Point to be checked.
    #  \return True is the given Point lies on this Tile, False if not.
    def hasPoint( point ):
        pass

    ## \brief Checks if this Tile is a NullTile.
    #
    #  A NullTile is a Tile that should not be drawn at all
    #  because it is entirely transparent.
    #
    #  \return True is this Tile is a NullTile.
    def isNullTile():
        pass

    def getPointPointer( index ):
        pass

    def setSurface( index, surfaceCode ):
        pass

    def setSideSurface( sideSurfaceCode ):
        pass

    def setSideSurfaceOffset( sso ):
        pass

    def getSurface( index ):
        pass

    def getSideSurface():
        pass

    def getSideSurfaceOffset():
        pass
