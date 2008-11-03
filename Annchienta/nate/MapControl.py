import annchienta
import MapView

## A class that controls, edits and holds the Map.
#
class MapControl:

    def __init__( self ):

        # The current map
        self.currentMap = None 

        # Get some references
        self.engine     = annchienta.getEngine()
        self.mapManager = annchienta.getMapManager()

        # Create a MapView
        self.mapView = MapView.MapView()

    def getMap( self ):
        return self.currentMap

    def loadMap( self, filename ):

        # Make sure the map is valid.
        if self.engine.isValidFile( filename ):

            # Load the map... use False because we don't want scrips
            self.currentMap = annchienta.Map( filename, False )
