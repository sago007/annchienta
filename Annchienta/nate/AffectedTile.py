## A tile that is affected by an edit.
#
class AffectedTile:

    def __init__( self, tile, points ):

        # Store tile
        self.tile = tile

        # Store points
        self.points = points

    def getTile( self ):
        return self.tile

    def getPoints( self ):
        return self.points
