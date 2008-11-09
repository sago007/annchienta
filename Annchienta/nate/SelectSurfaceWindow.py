import gtk
import gtk.glade

class SelectSurfaceWindow:

    # Number of columns
    COLUMNS = 3

    def __init__( self, side ):

        # If we're dealing with a side surface selection thingy
        self.side = side

        # Glade file
        self.gladefile = "SelectSurfaceWindow.glade"

        # Load widget tree
        self.widgetTree = gtk.glade.XML( self.gladefile )

        dic = { "on_window_delete_event":       self.close }

        # Connect
        self.widgetTree.signal_autoconnect( dic )

        # Get window and table
        self.window = self.widgetTree.get_widget("window")
        self.table = self.widgetTree.get_widget("table")

        # Keep track of the children
        self.children = []

        # Selected surface
        self.selectedSurface = 0

    def show( self ):
        self.window.show()

    def close( self, widget=None, event=None ):
        self.window.hide()
        return True

    ## Creates a good table
    #
    def create( self, tileSet ):

        # Clear everything
        for child in self.children:
            self.table.remove( child )

        self.children = []

        # Calculate how much we need
        size = tileSet.getNumberOfSideSurfaces() if self.side else tileSet.getNumberOfSurfaces()

        # Calculate rows
        rows = int( size / self.COLUMNS )

        self.table.resize( rows, self.COLUMNS )

        for i in range( size ):

            # Calculate position in table
            y = int( i / self.COLUMNS )
            x = i % self.COLUMNS

            # Determine filename
            fileName = tileSet.getDirectory() + '/'
            if self.side:
                fileName += 'side'
            fileName += str(i) + '.png'

            # Create image
            image = gtk.Image()
            image.set_from_file( fileName )
            image.show()

            # Add image to button
            button = gtk.Button()
            button.add( image )
            button.connect("clicked", self.surfaceClicked, i )
            button.show()

            self.table.attach( button, x, x+1, y, y+1 )
            self.children += [button]

    def surfaceClicked( self, widget=None, data=None ):
        self.selectedSurface = int(data)

    def getSelectedSurface( self ):
        return self.selectedSurface

# TEST
if __name__ == "__main__":

    surfaceWindow = SelectSurfaceWindow( False )
    surfaceWindow.show()
    gtk.main()

