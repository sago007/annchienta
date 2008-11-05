import annchienta

## Holds an annchienta video window
#  that displays the map.
class MapView:

    # Simple enum
    NO_DRAW_GRID = 0
    SIMPLE_DRAW_GRID = 1
    HEIGHT_DRAW_GRID = 2

    def __init__( self ):

        # Currently viewed map.
        self.currentMap = None

        # Get a few references.
        self.videoManager = annchienta.getVideoManager()
        self.mapManager   = annchienta.getMapManager()

        # Set the video mode
        self.videoManager.setVideoMode( 640, 480, "NATE - Map View" )

        # Initial camera position
        self.cameraPosition = annchienta.Vector( 0, 0 )

        # Draw grid method
        self.drawGridType = self.SIMPLE_DRAW_GRID

    ## Free up stuff
    #
    def free( self ):
        self.currentMap = None

    ## Sets the map to be viewed
    #
    def setMap( self, currentMap ):
        self.currentMap = currentMap

    ## Get camera position
    #
    def getCameraPosition( self ):
        return self.cameraPosition

    ## Set camera position
    #
    def setCameraPosition( self, cameraPosition ):
        self.cameraPosition = cameraPosition

    ## Set draw grid type
    #
    def setDrawGridType( self, drawGridType ):
        self.drawGridType = drawGridType

    ## Draws the map
    #
    def draw( self ):

        # Only draw if there is a map
        if self.currentMap:

            self.videoManager.begin()

            # Get a decent camera position
            self.videoManager.translate( -self.cameraPosition.x, -self.cameraPosition.y )

            # Draw the son of a bitch
            self.currentMap.draw( False )

            # Draw a type of grid
            if self.drawGridType == self.SIMPLE_DRAW_GRID:
                self.drawSimpleGrid()
            elif self.drawGridType == self.HEIGHT_DRAW_GRID:
                self.drawHeightGrid()

            self.videoManager.end()

    ## Draw a very simple grid
    #
    def drawSimpleGrid( self ):

        self.videoManager.pushMatrix()

        # Get the current layer and go to position
        layer = self.currentMap.getCurrentLayer()
        self.videoManager.translate( 0, -layer.getZ() )

        # Pick a color for the grid
        self.videoManager.setColor( 255, 255, 255 )

        # Draw x-aligned lines
        for y in range( 1, layer.getHeight() ):
            p1 = layer.getTile( 0, y ).getPointPointer( 0 )
            p2 = layer.getTile( layer.getWidth()-1, y ).getPointPointer( 3 )
            self.videoManager.drawLine( p1.x, p1.y, p2.x, p2.y )

        # Draw y-aligned lines
        for x in range( 1, layer.getWidth() ):
            p1 = layer.getTile( x, 0 ).getPointPointer( 0 )
            p2 = layer.getTile( x, layer.getHeight()-1 ).getPointPointer( 1 )
            self.videoManager.drawLine( p1.x, p1.y, p2.x, p2.y )
            
        self.videoManager.popMatrix()

    ## Draw a height-based grid
    #
    def drawHeightGrid( self ):

        self.videoManager.pushMatrix()

        # Get the current layer and go to position
        layer = self.currentMap.getCurrentLayer()
        self.videoManager.translate( 0, -layer.getZ() )

        # Pick a color for the grid
        self.videoManager.setColor( 255, 255, 255 )

        # Loop through all tiles.
        for y in range( layer.getHeight() ):
            for x in range( layer.getWidth() ):

                tile = layer.getTile( x, y )

                # Get all tilepoints, converted to screenpoints
                tilePoints = map( lambda i: tile.getPointPointer(i).to( annchienta.ScreenPoint ), range(4) )

                # Now draw lines
                for i in range(4):
                    p1 = tilePoints[i]
                    p2 = tilePoints[ (i+1)%4 ]
                    self.videoManager.drawLine( p1.x, p1.y, p2.x, p2.y )

        self.videoManager.popMatrix()

