import annchienta
import AffectedTile

class TileSelection:

    def __init__( self, mapControl ):

        # References
        self.inputManager = annchienta.getInputManager()
        self.mapManager   = annchienta.getMapManager()

        # Store mapcontrol
        self.mapControl = mapControl

        # Set parameters
        self.selectWholeTiles( True )
        self.setRadius( 32 )

    ## Set to true or false
    #
    def selectWholeTiles( self, wholeTiles ):
        self.wholeTiles = wholeTiles

    ## The radius of the selection
    #
    def setRadius( self, radius ):
        self.radius = radius
        self.squaredRadius = radius*radius

    ## Get the current selection. Returns
    #  a list of AffectedTile's.
    def getSelection( self ):

        # Get layer and mapview
        layer = self.mapControl.getMap().getCurrentLayer()
        cameraPosition = self.mapControl.getMapView().getCameraPosition()

        # Set mouse position
        mousePosition = annchienta.Point( annchienta.MapPoint, self.inputManager.getMouseX(), self.inputManager.getMouseY() )
        mousePosition.x += int(cameraPosition.x)
        mousePosition.y += int(cameraPosition.y)

        # Little adjust
        if self.wholeTiles:
            mousePosition.y -= self.mapManager.getTileHeight()/2

        # Initialize list
        affectedTiles = []

        # Loop through all tiles
        for y in range( layer.getHeight() ):
            for x in range( layer.getWidth() ):

                tile = layer.getTile( x, y )

                # Select an entire tile
                if self.wholeTiles:
                    p = tile.getPointPointer( 0 )
                    if p.noTypeCheckSquaredDistance( mousePosition ) < self.squaredRadius:
                        affectedTiles.append( AffectedTile.AffectedTile( tile, range(4) ) )

                # Select points of a tile
                else:
                    points = []
                    for i in range(4):
                        p = tile.getPointPointer(i)
                        if p.noTypeCheckSquaredDistance( mousePosition ) < self.squaredRadius:
                            points.append(i)
                    if len( points ):
                        affectedTiles.append( AffectedTile.AffectedTile( tile, points ) )

        return affectedTiles
