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
    def draw( self, drawObstructionGrid=False ):

        # Only draw if there is a map
        if self.currentMap:

            self.videoManager.clear()

            # Get a decent camera position
            self.videoManager.translate( -self.cameraPosition.x, -self.cameraPosition.y )

            # Draw the son of a bitch
            self.currentMap.draw( False )

            # Draw a type of grid
            if self.drawGridType == self.SIMPLE_DRAW_GRID:
                self.drawSimpleGrid()
            elif self.drawGridType == self.HEIGHT_DRAW_GRID:
                self.drawHeightGrid()

            # Draw obstruction grid
            if drawObstructionGrid:
                self.drawObstructionGrid()

            self.videoManager.flip()

    ## Draw a very simple grid
    #
    def drawSimpleGrid( self ):

        self.videoManager.push()

        # Get the current layer and go to position
        layer = self.currentMap.getCurrentLayer()
        self.videoManager.translate( 0, -layer.getZ() )

        # Pick a color for the grid
        self.videoManager.setColor( 255, 255, 255 )

        # Draw x-aligned lines
        for y in range( 1, layer.getHeight() ):
            p1 = layer.getTile( 0, y ).getPointPointer( 0 )
            p2 = layer.getTile( layer.getWidth()-1, y ).getPointPointer( 3 )
            self.videoManager.drawLine( int(p1.x), int(p1.y), int(p2.x), int(p2.y) )

        # Draw y-aligned lines
        for x in range( 1, layer.getWidth() ):
            p1 = layer.getTile( x, 0 ).getPointPointer( 0 )
            p2 = layer.getTile( x, layer.getHeight()-1 ).getPointPointer( 1 )
            self.videoManager.drawLine( int(p1.x), int(p1.y), int(p2.x), int(p2.y) )
            
        self.videoManager.pop()

    ## Draw a height-based grid
    #
    def drawHeightGrid( self ):

        self.videoManager.push()

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
                    self.videoManager.drawLine( int(p1.x), int(p1.y), int(p2.x), int(p2.y) )

        self.videoManager.pop()

    ## Draw an obstruction grid
    #
    def drawObstructionGrid( self ):

        self.videoManager.push()

        # Get the current layer and go to position
        layer = self.currentMap.getCurrentLayer()
        self.videoManager.translate( 0, -layer.getZ() )

        # Loop through all tiles.
        for y in range( layer.getHeight() ):
            for x in range( layer.getWidth() ):

                tile = layer.getTile( x, y )

                # Only draw if not default 
                if tile.getObstructionType() != annchienta.DefaultObstruction:

                    # Get all tilepoints, converted to mappoints
                    tilePoints = map( lambda i: tile.getPointPointer(i).to( annchienta.MapPoint ), range(4) )

                    # Selected color based on ObstructionType
                    if tile.getObstructionType() == annchienta.NoObstruction:
                        self.videoManager.setColor( 0, 255, 0, 100 )
                    else:
                        self.videoManager.setColor( 255, 0, 0, 100 )

                    # Draw a quad
                    self.videoManager.drawQuad( tilePoints[0].x, tilePoints[0].y,
                                                tilePoints[1].x, tilePoints[1].y,
                                                tilePoints[2].x, tilePoints[2].y,
                                                tilePoints[3].x, tilePoints[3].y,
                                              )

        self.videoManager.pop()


