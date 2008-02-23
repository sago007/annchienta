
class AffectedTile:

    def __init__( self, tile, p0, p1, p2, p3 ):

        self.tile = tile
        self.points = []

        if p0:
            self.points.append(0)
        if p1:
            self.points.append(1)
        if p2:
            self.points.append(2)
        if p3:
            self.points.append(3)

class Selection:

    def __init__(self):

        self.clear()

    def clear(self):

        self.tiles = []
