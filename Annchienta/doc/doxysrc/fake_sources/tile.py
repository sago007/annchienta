
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

    ## \brief Sets Z value of a Point.
    #
    #  \param index Index of the Point of which you want to change the Z coord.
    #  \param z The new Z value for that Point.
    def setZ( index, z ):
        pass

    ## \brief Gets Z value of a Point.
    #
    #  \param index Index of the Point of which you want to retrieve the Z coord.
    #  \return The Z value of that Point.
    def getZ( index ):
        pass

    ## \brief Gets a reference to a Point of this tile.
    #
    #  \param index Index of the Point you want to retrieve.
    #  \return One of the Points of this Tile.
    def getPointPointer( index ):
        pass

    ## \brief Sets the Top Surface.
    #
    #  \param index Index of the Point this Surface needs to be asigned to.
    #  \param surfaceNumber Number of the Surface you want in the TileSet being used in this Map.
    def setSurface( index, surfaceNumber ):
        pass

    ## \brief Sets the Side Surface.
    #
    #  \param sideSurfaceNumber Number of the SideSurface you want in the TileSet being used in this Map.
    def setSideSurface( sideSurfaceNumber ):
        pass

    ## \brief Sets Side Surface offset.
    #
    #  By default, the Side Surface starts at the top of the Tile
    #  goes until the ground. By setting this offset value, the
    #  Side Surface will only go to this offset instead of to the
    #  ground.
    #
    #  \param sso The new Side Surface offset.
    def setSideSurfaceOffset( sso ):
        pass

    ## \brief Gets the Surface.
    #
    #  \param index Index of the Point of which you want the Surface.
    #  \return Number of the Surface used.
    def getSurface( index ):
        pass

    ## \brief Gets the Side Surface.
    #
    #  \return Number of the SideSurface being used.
    def getSideSurface():
        pass

    ## \brief Gets the Side Surface offset.
    #
    #  \return The Side Surface offset. See setSideSurfaceOffset().
    def getSideSurfaceOffset():
        pass

    ## \brief Sets the ObstructionType.
    #
    #  There are three possibilities:
    #
    #  \li DefaultObstruction
    #
    #  The default value. Persons will be able to step on this Tile,
    #  depending on the height and the values set by
    #  MapManager.setMaxAscentHeight() and
    #  MapManager.setMaxDescentHeight().
    #
    #  \li NoObstruction
    #
    #  All Persons will always be able to step on this Tile,
    #  regardless of it's height.
    #
    #  \li FullObstruction
    #
    #  Nobody will ever be able to step on this Tile,
    #  regardless of it's height.
    #
    #  \param obstructionType The new ObstructionType for this tile.
    def setObstructionType( obstructionType ):
        pass

    ## \brief Gets the ObstructionType.
    #
    #  See setObstructionType().
    #
    #  \return The current ObstructionType.
    def getObstructionType():
        pass

