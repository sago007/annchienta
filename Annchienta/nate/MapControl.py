import annchienta
import MapView

## A class that controls, edits and holds the Map.
#
class MapControl:

    ## Create a new MapControl.
    #
    def __init__( self ):

        # The current map
        self.currentMap = None 

        # Get some references
        self.engine     = annchienta.getEngine()
        self.mapManager = annchienta.getMapManager()

        # Create a MapView
        self.mapView = MapView.MapView()

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
            self.currentMap = annchienta.Map( filename, False )

            # Pass the map to the MapView
            self.mapView.setMap( self.currentMap )

    ## Create a new map.
    #  \param width Width of the Map.
    #  \param height Height of the Map.
    #  \param tilesetDirectory Where the tileset can be found.
    #
    def createMap( self, width, height, tilesetDirectory ):

        # Create the map
        self.currentMap = annchienta.Map( width, height, tilesetDirectory )

        # Pass the map to the MapView
        self.mapView.setMap( self.currentMap )

