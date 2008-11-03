import pygtk
import gtk
import gtk.glade
import os
import annchienta
import MapControl

class MainWindow:

    ## Creates a new MainWindow instance.
    #
    def __init__( self ):

        # Get a few annchienta references
        self.mapManager = annchienta.getMapManager()

        # The instance that controls the map
        self.mapControl = MapControl.MapControl()

        # Glade file we'll be using
        self.gladefile = "MainWindow.glade"

        # Create glade instance
        self.widgetTree = gtk.glade.XML( self.gladefile )

        # Create a dictionary for events
        dic = { "on_window_delete_event":                              self.close,
                "on_gameWorkingDirectoryChooser_selection_changed":    self.updateGameWorkingDirectory,
                "on_tileWidthSpinButton_value_changed":                self.updateTileWidth }

        # Connect that dictionary
        self.widgetTree.signal_autoconnect( dic )

    ## Closes this window, exiting the editor.
    #
    def close( self, widget=None, event=None ):
        gtk.main_quit()

    ## Updates the working directory for the game.
    #
    def updateGameWorkingDirectory( self, widget=None ):
        # Cd to that directory
        os.chdir( widget.get_current_folder() )

    ## Updates the tile width
    #
    def updateTileWidth( self, widget=None ):
        # Update the mapmanager tilesizes
        value = widget.get_value_as_int()
        self.mapManager.setTileWidth( value )
        self.mapManager.setTileHeight( int(value/2) )

