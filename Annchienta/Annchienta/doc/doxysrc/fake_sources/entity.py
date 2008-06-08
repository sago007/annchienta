
## \brief Holds an Entity.
#
#  This class is an abstract superclass for Tiles,
#  StaticObjects and Persons.
class Entity:

    ## \brief Creates a new Entity.
    #
    #  \param name The name for this Entity.
    #  \return A newly created Entity.
    def __init__( name ):
        pass

    ## \brief Returns the Entity Type.
    #
    #  \return TileEntity, StaticObjectEntity or PersonEntity.
    def getEntityType():
        pass

    ## \brief Renders this Entity.
    #
    def draw():
        pass

    ## \brief Updates this Entity.
    #
    def update():
        pass

    ## \brief Gets the depth from the origin.
    #
    #  This is used to draw all entities in the correct
    #  order. Lower depth = farther from the screen
    #  \return The depth of this Entity.
    def getDepth():
        pass

    ## \brief The poition of the Entity Mask.
    #
    #  \return A Point referring to where the Mask of this entity should be drawn.
    def getMaskPosition():
        pass

    ## \brief Sets this Entity as drawn.
    #
    #  \param value When set to True, the Entity will not be drawn this render because the engine assumes it has been drawn already.
    def setDrawn( value ):
        pass

    ## \brief Checks if this Entity has been drawn.
    #
    #  \return True if this Entity was already drawn in the current render.
    def isDrawn():
        pass

    ## \brief Sets the name of this Entity.
    #
    #  \param name The new name for this Entity.
    def setName( name ):
        pass

    ## \brief Gets the name of this Entity.
    #
    #  \return The name of this Entity.
    def getName():
        pass

    ## \brief Sets the Layer of this Entity.
    #
    #  This happens automatically when using
    #  Layer.addEntity()
    #
    #  \param layer The new Layer to which this Entity should belong.
    def setLayer( layer ):
        pass

    ## \brief Gets a reference to the Layer of this Entity.
    #
    #  \return The Layer to which this Entity belongs.
    def getLayer():
        pass
