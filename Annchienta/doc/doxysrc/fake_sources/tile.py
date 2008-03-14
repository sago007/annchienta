
## \brief Holds a Tile.
#
#  This class is used to hold parts of the Layer, called tiles.
#  Because we are using an isometric system, tiles are usually
#  shaped like a rhombus.
#
#  A Tile consist of four Points, indexed like this:
#  \image html tile_pointindexes.png
#
#  A Tile has a top Surface and a Side Surface.
#  \image html tile_anatomy.png
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

    ## \brief Gets a reference to a Point of this tile.
    #
    #  \param index Index of the Point you want to retrieve.
    #  \return One of the Points of this Tile.
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
