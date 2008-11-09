import pygtk
import gtk
import gtk.glade
import os
import annchienta
import MapControl
import MapView
import NewMapWindow

class MainWindow:

    ## Creates a new MainWindow instance.
    #
    def __init__( self ):

        # Get a few annchienta references
        self.mapManager = annchienta.getMapManager()

        # The instance that controls the map
        self.mapControl = MapControl.MapControl( self )

        # A window to create new maps
        self.newMapWindow = NewMapWindow.NewMapWindow( self.mapControl )

        # Glade file we'll be using
        self.gladefile = "MainWindow.glade"

        # Create glade instance
        self.widgetTree = gtk.glade.XML( self.gladefile )

        # Create a dictionary for events
        dic = { "on_window_delete_event":                              self.close,
                "on_gameWorkingDirectoryChooser_selection_changed":    self.updateGameWorkingDirectory,
                "on_tileWidthSpinButton_value_changed":                self.updateTileWidth,
                "on_drawGridComboBox_changed":                         self.updateDrawGrid,

                "on_createNewMapButton_clicked":                       self.createNewMap,
                "on_openMapFileChooser_selection_changed":             self.updateMapFile,
                "on_nextLayerButton_clicked":                          self.nextLayer,
                "on_addLayerButton_clicked":                           self.addLayer,
                "on_changeLayerZSpinButton_value_changed":             self.updateLayerZ,

                "on_editWholeTilesCheckButton_toggled":                self.updateWholeTiles,
                "on_editRadiusSpinButton_value_changed":               self.updateEditRadius,

                "on_showTilesWindowButton_clicked":                    self.showTilesWindow,
                "on_showSidesWindowButton_clicked":                    self.showSidesWindow }

        # Connect that dictionary
        self.widgetTree.signal_autoconnect( dic )

    ## Closes this window, exiting the editor.
    #
    def close( self, widget=None, event=None ):
        gtk.main_quit()
        return True

    ## Free up some files to avoid segmentation faults
    #
    def free( self ):
        self.mapControl.free()

    ## Updates the working directory for the game.
    #
    def updateGameWorkingDirectory( self, widget=None ):
        # Cd to that directory
        os.chdir( str(widget.get_filename()) )

    ## Updates the tile width
    #
    def updateTileWidth( self, widget=None ):
        # Update the mapmanager tilesizes
        value = widget.get_value_as_int()
        self.mapManager.setTileWidth( value )
        self.mapManager.setTileHeight( int(value/2) )

    ## Updates the way to draw grids
    #
    def updateDrawGrid( self, widget=None ):

        # Retrieve the grid type from a dictionary
        dic = { 0: MapView.MapView.NO_DRAW_GRID,
                1: MapView.MapView.SIMPLE_DRAW_GRID,
                2: MapView.MapView.HEIGHT_DRAW_GRID }
        self.mapControl.getMapView().setDrawGridType( dic[ int(widget.get_active()) ] )

    ## Creates a new window that gives options to
    #  create a new map.
    def createNewMap( self, widget=None ):
        self.newMapWindow.show()

    ## Updates the map file, creating a new map
    #  if necessary
    def updateMapFile( self, widget=None ):

        filename = str(widget.get_filename())
        self.mapControl.loadMap( filename )

    ## Cycle to next layer
    #
    def nextLayer( self, widget=None ):
        self.mapControl.nextLayer()

    ## Add a new layer
    #
    def addLayer( self, widget=None ):
        self.mapControl.addLayer()

    ## Update the Z of the current layer
    #
    def updateLayerZ( self, widget=None ):
        z = int( widget.get_value_as_int() )
        self.mapControl.setLayerZ( z )

    ## Change whether we edit whole tiles or not
    #
    def updateWholeTiles( self, widget=None ):
        tileSelection = self.mapControl.getTileSelection()
        tileSelection.selectWholeTiles( widget.get_active() )

    ## Set the edit radius
    #
    def updateEditRadius( self, widget=None ):
        tileSelection = self.mapControl.getTileSelection()
        tileSelection.setRadius( int( widget.get_value_as_int() ) )

    ## Show tiles window
    #
    def showTilesWindow( self, widget=None ):
        self.mapControl.showSelectSurfaceWindow()

    ## Show tiles sides window
    #
    def showSidesWindow( self, widget=None ):
        self.mapControl.showSelectSideSurfaceWindow()

    ## Change the value in the spin box
    #
    def setLayerZValue( self, z ):
        widget = self.widgetTree.get_widget("changeLayerZSpinButton")
        widget.set_value( float(z) )

    ## Look if we should edit tile Z
    #
    def editZChecked( self ):
        widget = self.widgetTree.get_widget("editZCheckButton")
        return widget.get_active()

    ## The Z we should set.
    #
    def getEditZ( self ):
        widget = self.widgetTree.get_widget("editZSpinButton")
        return int( widget.get_value_as_int() )

    ## Look if we should edit tile surfaces
    #
    def editTilesChecked( self ):
        widget = self.widgetTree.get_widget("editTilesCheckButton")
        return widget.get_active()

    ## Look if we should edit tile side surfaces
    #
    def editSidesChecked( self ):
        widget = self.widgetTree.get_widget("editSidesCheckButton")
        return widget.get_active()

