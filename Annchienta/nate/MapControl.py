import annchienta
import MapView
import MapWriter
import TileSelection
import SelectSurfaceWindow
import gobject
import gtk

## A class that controls, edits and holds the Map.
#
class MapControl:

    ## Create a new MapControl.
    #
    def __init__( self, mainWindow):

        # The current map
        self.currentMap = None 

        # Keep the mainWindow too
        self.mainWindow = mainWindow

        # Get some references
        self.engine       = annchienta.getEngine()
        self.inputManager = annchienta.getInputManager()

        # Create a MapView
        self.mapView = MapView.MapView()

        # The MapWrite we'll use, constructed when we load/create
        # a map.
        self.mapWriter = None

        # Use this to get a tile selection
        self.tileSelection = TileSelection.TileSelection( self )

        # Two windows to select surfaces.
        self.selectSurfaceWindow = SelectSurfaceWindow.SelectSurfaceWindow( False )
        self.selectSideSurfaceWindow = SelectSurfaceWindow.SelectSurfaceWindow( True )

        # Start a function that updates ourselve.
        gobject.timeout_add( 100, self.tick )

        # The previous mouse position, used for camera calculations
        self.mousePosition = None 

    ## Free up stuff
    #
    def free( self ):
        self.currentMap = None
        self.mapView.free()

    ## Get a reference to the MapView
    #
    def getMapView( self ):
        return self.mapView

    ## Get a reference to the TileSelection
    #
    def getTileSelection( self ):
        return self.tileSelection

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

            # Create writer
            self.mapWriter = MapWriter.MapWriter( loadedMap, filename )

    ## Create a new map.
    #  \param width Width of the Map.
    #  \param height Height of the Map.
    #  \param tilesetDirectory Where the tileset can be found. (relative path would be best)
    #
    def createMap( self, width, height, tileSetDirectory ):

        # Create the map
        createdMap = annchienta.Map( width, height, tileSetDirectory )

        self.setMap( createdMap )

        # Create writer
        self.mapWriter = MapWriter.MapWriter( createdMap )

    ## Sets the map
    #
    def setMap( self, currentMap ):

        # set it
        self.currentMap = currentMap
        # Do a depthsorth
        self.currentMap.depthSort()
        # pass
        self.mapView.setMap( currentMap )
        # Set surface select windows
        self.selectSurfaceWindow.create( self.currentMap.getTileSet() )
        self.selectSideSurfaceWindow.create( self.currentMap.getTileSet() )

    ## Saves the map
    #
    def saveMap( self ):

        if self.currentMap and self.mapWriter:
            self.mapWriter.saveMap()

    ## Ticks this object. This will update this and
    #  all of it's associated objects.
    def tick( self ):

        # Call the general update function
        self.update()

        # Draw everything
        self.draw()

        # Quit the main function if we quit the annchienta
        # engine (User closed vide window)
        if not self.inputManager.running() and gtk.main_level():
            gtk.main_quit()

        # Return true because this gets called though
        # a gobject callback and we want it too keep
        # running.
        return True

    ## A rather general update function
    #
    def update( self ):

        # Update the inputmanager
        self.inputManager.update()

        newMousePosition = annchienta.Vector( self.inputManager.getMouseX(), self.inputManager.getMouseY() )
        if self.mousePosition:
            # Translate view with right mouse button
            if self.inputManager.buttonDown(1):
                diff = self.mousePosition - newMousePosition
                diff += self.mapView.getCameraPosition()
                self.mapView.setCameraPosition( diff )

        # Check if we have to make edits.
        if self.currentMap and self.inputManager.buttonDown(0):

            # Get the selection
            selection = self.tileSelection.getSelection()

            for affected in selection:

                tile = affected.getTile()

                # Check if we have to edit side surfaces
                if self.mainWindow.editSidesChecked():
                    tile.setSideSurface( self.selectSideSurfaceWindow.getSelectedSurface() )

                for point in affected.getPoints():

                    # Check if we have to edit Z coordinates
                    if self.mainWindow.editZChecked():
                        tile.setZ( point, self.mainWindow.getEditZ() )

                    # Check if we have to edit tiles
                    if self.mainWindow.editTilesChecked():
                        tile.setSurface( point, self.selectSurfaceWindow.getSelectedSurface() )
        
        self.mousePosition = newMousePosition

    ## Draw stuff
    #
    def draw( self ):

        self.mapView.draw()

    ## Cycle to next layer
    #
    def nextLayer( self ):

        if self.currentMap:
            index = self.currentMap.getCurrentLayerIndex()
            index = (index + 1) % self.currentMap.getNumberOfLayers()
            self.currentMap.setCurrentLayer( index )
            # Update the spinbox
            self.mainWindow.setLayerZValue( self.currentMap.getCurrentLayer().getZ() )

    ## Add a new layer
    #
    def addLayer( self ):
        if self.currentMap:
            self.currentMap.addNewLayer()

    ## Adjust the Z offset of the current layer
    #
    def setLayerZ( self, z ):
        self.currentMap.getCurrentLayer().setZ( z )

    ## Show surface window
    #
    def showSelectSurfaceWindow( self ):
        self.selectSurfaceWindow.show()

    ## Show side surface window
    #
    def showSelectSideSurfaceWindow( self ):
        self.selectSideSurfaceWindow.show()
