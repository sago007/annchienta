
## \brief Obtain the MapManager instance.
#
#  Use this function to get access to the MapManager
#  instance anywhere.
#
#  \return The global MapManager instance.
def getMapManager():
    pass


## \brief Handles the map.
#
#  Use this class to control various maps and their
#  behaviour.
class MapManager:

    ## \brief Sets the tile width.
    #
    #  \param tileWidth The new tile width.
    def setTileWidth( tileWidth ):
        pass

    ## \brief Gets the tile width.
    #
    #  \return The current tile width.
    def getTileWidth():
        pass

    ## \brief Sets the tile height.
    #
    #  \param tileHeight The new tile height.
    def setTileHeight( tileHeight ):
        pass

    ## \brief Gets the tile height.
    #
    #  \return The current tile height.
    def getTileHeight():
        pass

    ## \brief Sets the camera X coordinate.
    #
    #  \param x The new camera X coordinate.
    def setCameraX( x ):
        pass

    ## \brief Gets the camera X coordinate.
    #
    #  \return The current camera X coordinate.
    def getCameraX():
        pass

    ## \brief Sets the camera Y coordinate.
    #
    #  \param y The new camera Y coordinate.
    def setCameraX( y ):
        pass

    ## \brief Gets the camera Y coordinate.
    #
    #  \return The current camera Y coordinate.
    def getCameraY():
        pass

    ## \brief Makes the camera follow an object.
    #
    #  \param object The StaticObject or Person the camera needs to follow.
    def cameraFollow( object ):
        pass

    ## \brief Makes the camera take a peek at an object.
    #
    #  The camera will only look at this object until update() is
    #  called. After that, it will look at the object set with
    #  cameraFollow( object ) again.
    #
    #  \param object The StaticObject or Person the camera needs to peek at.
    def cameraPeekAt( object ):
        pass

    ## \brief Sets the number of updates per second.
    #
    #  While the framerate is variable, the number of updates per
    #  second is not. 60 should be a good value.
    #
    #  \param rate The update rate.
    def setUpdatesPerSecond( rate ):
        pass

    ## \brief Sets the current Map.
    #
    #  This should be called in the beginning of your game,
    #  and when the player moves to a next Map.
    #
    #  \code
    # myMap = annchienta.Map( "data/maps/mymap.xml" )
    # mapManager.setCurrentMap( myMap )
    #  \endcode
    #
    #  \param map The new Map to be set.
    def setCurrentMap( map ):
        pass

    ## \brief Get the current Map.
    #
    #  \return A reference to the current map.
    def getCurrentMap():
        pass

    ## \brief Sets maximum ascent height.
    #
    #  This variable is used for example when the player is trying
    #  to walk up a slope. He will only be able to do this when
    #  the difference between the height of the slope and his
    #  current height is smaller than the maximum ascent height.
    #  So simply put, the maximum height a player can climb in
    #  one step.
    #
    #  The maximum descent height is the same, but relevates to
    #  descending...
    #
    #  \param mah The new maximum ascent height.
    def setMaxAscentHeight( mah ):
        pass

    ## \brief Gets the maximum ascent height.
    #
    #  See setMaxAscentHeight() for an explanation of this
    #  variable.
    #
    #  \return The maximum ascent height.
    def getMaxAscentHeight():
        pass

    ## \brief Sets maximum descent height.
    #
    #  See setMaxAscentHeight() for an explanation of this
    #  variable.
    #
    #  \param mdh The new maximum descent height.
    def setMaxDescentHeight( mdh ):
        pass

    ## \brief Gets the maximum descent height.
    #
    #  See setMaxAscentHeight() for an explanation of this
    #  variable.
    #
    #  \return The maximum descent height.
    def getMaxDescentHeight():
        pass

    ## \brief Retrieve an object by it's name.
    #
    #  Search for a Person or StaticObject in the current
    #  Map and return it. If there are multiple objects with this
    #  name, the first one found will be returned.
    #
    #  \param name Name of the object to search for.
    #  \return The Person or StaticObject with the given name.
    def getObject( name ):
        pass

    ## \brief Set script to be executed every update.
    #
    #  \param script This script will be executed every update from now on.
    def setOnUpdateScript( script ):
        pass

    ## \brief Set code to be executed every update.
    #
    #  \param code This piece of code will be executed every update from now on.
    def setOnUpdateCode( code ):
        pass

    ## \brief Start the MapManager.
    #
    #  This basically runs the game. It does not return until
    #  the game is quitted or finished...
    def run():
        pass

    ## \brief Updates the current MapManager.
    #
    #  This function updates the MapManager a few times, or not
    #  even once, this all depends on the time passed since the
    #  last update. So use this function when you do not want to
    #  disturb the game's timing, else, use updateOnce().
    #
    #  \param updateInput Whether the input should be updates as well or not.
    def update( updateInput=True ):
        pass

    ## \brief Updates the current MapManager once.
    #
    #  See explanation with update(). You will probably want
    #  to call resync() after using this.
    #
    #  \param updateInput Whether the input should be updates as well or not.
    def updateOnce( updateInput=True ):
        pass

    ## \brief Renders a frame.
    #
    #  Draws the current Map with all the entities in it.
    def renderFrame():
        pass

    ## \brief Renders a terrain frame.
    #
    #  Same as renderFrame() but this function only renders tiles.
    def renderTerrain():
        pass

    ## \brief Resyncs update timing.
    #
    #  Use this function whenever you disturbed timing. After
    #  calling this, all timing should be back in order.
    def resync():
        pass


