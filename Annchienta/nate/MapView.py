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

    ## Sets the map to be viewed
    #
    def setMap( self, currentMap ):
        self.currentMap = currentMap
