
## \brief Holds a Map.
#
#  This class is used for holding maps.
#
class Map:

    ## \brief Loads a Map.
    #
    #  This function loads a Map from a valid Map XML file.
    #  \param filename XML file to be loaded.
    #  \return A new Map.
    def __init__( filename ):
        pass

    ## \brief Creates a new Map.
    #
    #  This function creates a new Map from scratch. This newly created
    #  Map will already contain one new Layer.
    #  \param width The width of the Map to be created.
    #  \param height The height of the Map to be created.
    #  \param tileSetDirectory The directory in which the tiles are situated.
    #  \return A new Map.
    def __init__( width, height, tileSetDirectory ):
        pass

    ## \brief Gets a reference to the current Layer.
    #
    #  \return The current Layer.
    def getCurrentLayer():
        pass

    ## \brief Gets a reference to a Layer in the Map.
    #
    #  \param index Index of the Layer to be returned.
    #  \return The Layer at the given index.
    def getLayer( index ):
        pass

    ## \brief Gets the index of the current Layer.
    #
    #  \return The index of the current Layer.
    def getCurrentLayerIndex():
        pass

    ## \brief Sets the current Layer.
    #
    #  \param index Index of the Layer to become the current Layer.
    def setCurrentLayer( index ):
        pass

    ## \brief Gets the number of Layers.
    #
    #  \return The number of Layers in this Map.
    def getNumberOfLayers():
        pass

    ## \brief Gets the filename.
    #
    #  \return The xml filename from which this map was loaded.
    def getFileName():
        pass

    ## \brief Gets the Map width.
    #
    #  \return The width of this Map.
    def getWidth():
        pass

    ## \brief Gets the Map height.
    #
    #  \return The height of this Map.
    def getHeight():
        pass

    ## \brief Adds a new Layer to this Map.
    #
    #  \param z The Z offset of the new Layer.
    def addNewLayer( z ):
        pass

    ## \brief Gets a reference to the TileSet used.
    #
    #  \return The TileSet used by this Map.
    def getTileSet():
        pass

    ## \brief Finds an object in this Map.
    #
    #  \param name The name of the Person or StaticObject to be found.
    #  \return The Person or StaticObject with the given name.
    def getObject( name ):
        pass

    ## \brief Adds an object.
    #
    #  The object given is added to the current Layer.
    #  \param object The Person or StaticObject to be added.
    def addObject( object ):
        pass

    ## \brief Removes an object.
    #
    #  \param object The Person or StaticObject to be removed.
    def removeObject( object ):
        pass

    ## \brief Updates the Map.
    #
    #  This function calls Layer.update() for all Layers.
    def update():
        pass

    ## \brief Draws the Map.
    #
    #  This function draws the Map and everything in it.
    def draw():
        pass

    ## \brief Draws the terrain.
    #
    #  This function only draws the tiles of this Map.
    def drawTerrain():
        pass

    ## \brief Sorts the Map.
    #
    #  This function calls Layer.depthSort() for all Layers.
    def depthSort():
        pass

    ## \brief Sorts the Layers.
    #
    #  This function performs a sort on all Layers to order them based
    #  on their Z offset so that they will be drawn in the correct
    #  order. This function does not modify Layer indexes used by
    #  getLayer().
    def sortLayers():
        pass

