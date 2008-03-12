
## \brief Holds a Map layer.
#
#  This class is used for holding layers in a Map.
#
class Layer:

    ## \brief Sets the layer opacity.
    #
    #  Default is 255.
    #
    #  \param opacity A value [0-255].
    def setOpacity( opacity ):
        pass

    ## \brief Gets the opacity.
    #
    #  \return The opacity of this layer.
    def getOpacity():
        pass

    ## \brief Sets the Z offset.
    #
    #  \param z The new Z offset.
    def setZ( z ):
        pass

    ## \brief Gets Z offset.
    #
    #  \return The Z offset.
    def getZ():
        pass

    ## \brief Updates this Layer.
    #
    #  Updating a Layer also updates all entities in it.
    def update():
        pass

    ## \brief Draws this Layer to the screen.
    #
    def draw():
        pass

    ## \brief Draws this terrain to the screen.
    #
    #  Same as draw(), but only draws the tiles.
    def drawTerrain():
        pass

    ## \brief Sorts all entities in the Layer.
    #
    #  This function sorts all entities in the Layer, so they will be
    #  drawn in the correct order.
    def depthSort():
        pass

    ## \brief Adds an Entity.
    #
    #  \param entity Entity to be added to this Layer.
    def addEntity( entity ):
        pass

    ## \brief Adds an Area.
    #
    #  \param area Area to be added to this Layer.
    def addArea( area ):
        pass

    ## \brief Gets width of this Layer.
    #
    #  \return The width of this Layer.
    def getWidth():
        pass

    ## \brief Gets height of this Layer.
    #
    #  \return The height of this Layer.
    def getWidth():
        pass

    ## \brief Gets a reference to a Tile.
    #
    #  \param x X coordinate of the Tile to be obtained.
    #  \param y Y coordinate of the Tile to be obtained.
    #  \return The Tile at the given position.
    def getTile( x, y ):
        pass

    ## \brief Gets a reference to an object.
    #
    #  \param index The index of the object you want.
    #  \return The StaticObject or Person at the given index.
    def getObject( index ):
        pass

    ## \brief Gets a reference to an object.
    #
    #  \param name The name of the object you want.
    #  \return The StaticObject or Person at the given index.
    def getObject( name ):
        pass

    ## \brief Counts the number of objects.
    #
    #  \return The number of StaticObjects and Persons.
    def getNumberOfObjects():
        pass

    ## \brief Removes an object from this Layer.
    #
    #  \param object The StaticObject or Person to be removed.
    def removeObject( object ):
        pass

    ## \brief Gets a reference to an Area.
    #
    #  \param index The index of the Area you want.
    def getArea( index ):
        pass
