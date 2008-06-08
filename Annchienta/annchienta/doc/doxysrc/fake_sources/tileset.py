
## \brief Holds Tiles.
#
#  This class is used for holding a number of Tile
#  Surfaces.
#
class TileSet:

    ## \brief Loads a new TileSet.
    #
    #  This function will load all Tile Surfaces and Tile
    #  Side Surfaces in the given directory. The Tile
    #  Surfaces must be called directory/{n}.png and the Tile
    #  Side Surfaces directory/side{n}.png, where n is an
    #  integer starting at 1. The Surfaces with number 0 are
    #  automatically generated and entirely transparent. For
    #  an explanation about Surfaces and Side Surfaces, see the
    #  Tile documentation.
    #
    def __init__( directory ):
        pass

    ## \brief Gets a Surface.
    #
    #  \param number Number of the Surface you want to retrieve.
    #  \return The Surface with the given number.
    def getSurface( number ):
        pass

    ## \brief Gets a Side Surface.
    #
    #  \param number Number of the Side Surface you want to retrieve.
    #  \return The Side Surface with the given number.
    def getSideSurface( number ):
        pass

    ## \brief Gets the Tile Mask.
    #
    #  \return A Mask used for Tile collisions.
    def getMask():
        pass

    ## \brief Gets the directory.
    #
    #  \return The directory in which these Surfaces are situated.
    def getDirectory():
        pass

