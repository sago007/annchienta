import annchienta
import MapView
import gobject
import gtk

## A class that controls, edits and holds the Map.
#
class MapControl:

    ## Create a new MapControl.
    #
    def __init__( self ):

        # The current map
        self.currentMap = None 

        # Get some references
        self.engine       = annchienta.getEngine()
        self.inputManager = annchienta.getInputManager()

        # Create a MapView
        self.mapView = MapView.MapView()

        # Start a function that updates ourselve.
        gobject.timeout_add( 100, self.tick )

    ## Free up stuff
    #
    def free( self ):
        self.currentMap = None
        self.mapView.free()

    ## Get the map.
    #
    def getMap( self ):
        return self.currentMap

    ## Load in the map with the given filename.
    #
    def loadMap( self, filename ):

        # Make sure the map is valid.
        if self.engine.isValidFile( filename ):

            # Load the map... use False because we don't want scrips
            loadedMap = annchienta.Map( filename, False )

            self.setMap( loadedMap )

    ## Create a new map.
    #  \param width Width of the Map.
    #  \param height Height of the Map.
    #  \param tilesetDirectory Where the tileset can be found.
    #
    def createMap( self, width, height, tilesetDirectory ):

        # Create the map
        createdMap = annchienta.Map( width, height, tilesetDirectory )

        self.setMap( createdMap )

    ## Sets the map
    #
    def setMap( self, currentMap ):

        # set it
        self.currentMap = currentMap
        # Do a depthsorth
        self.currentMap.depthSort()
        # pass
        self.mapView.setMap( currentMap )

    ## Ticks this object. This will update this and
    #  all of it's associated objects.
    def tick( self ):

        # Update the inputmanager
        self.inputManager.update()

        # Quit the main function if we quit the annchienta
        # engine (User closed vide window)
        if not self.inputManager.running() and gtk.main_level():
            gtk.main_quit()

        # Draw the map
        self.mapView.draw()

        # Return true because this gets called though
        # a gobject callback and we want it too keep
        # running.
        return True

