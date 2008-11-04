import annchienta

## Holds an annchienta video window
#  that displays the map.
class MapView:

    def __init__( self ):

        # Currently viewed map.
        self.currentMap = None

        # Get a few references.
        self.videoManager = annchienta.getVideoManager()

        # Set the video mode
        self.videoManager.setVideoMode( 640, 480, "NATE - Map View" )

        # Initial camera position
        self.cameraPosition = annchienta.Vector( 0, 0 )

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

            self.videoManager.end()
