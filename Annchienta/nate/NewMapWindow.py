import pygtk
import gtk
import gtk.glade
import os
import annchienta
import MapControl

class NewMapWindow:

    ## Creates a new NewMapWindow instance.
    #
    def __init__( self, mapControl ):

        # The instance that controls the map
        self.mapControl = mapControl

        # Glade file we'll be using
        self.gladefile = "NewMapWindow.glade"

        # Create glade instance
        self.widgetTree = gtk.glade.XML( self.gladefile )

        # Create a dictionary for events
        dic = { "on_window_delete_event":     self.hide,
                "on_confirmButton_clicked":   self.confirm }

        # Connect that dictionary
        self.widgetTree.signal_autoconnect( dic )

        # Get the main window
        self.window = self.widgetTree.get_widget("window")

    ## Hide this window, we might want to use it later 
    #
    def hide( self, widget=None, event=None ):
        self.window.hide()
        return True

    ## Show this window
    #
    def show( self ):
        self.window.show()

    ## Confirm the selection. This will create a new map
    #
    def confirm( self, widget=None ):

        # Get width from spinButton
        widthWidget = self.widgetTree.get_widget("mapWidthSpinButton")
        width = widthWidget.get_value_as_int()

        # Get height from spinButton
        heightWidget = self.widgetTree.get_widget("mapHeightSpinButton")
        height = heightWidget.get_value_as_int()

        # Get tileSet directory from filechooser button
        tileSetDirectoryWidget = self.widgetTree.get_widget("tileSetFileChooserButton")
        tileSetDirectory = str( tileSetDirectoryWidget.get_filename() )

        # Now create the map
        self.mapControl.createMap( width, height, tileSetDirectory )

        # Finally, close the window
        self.hide()

