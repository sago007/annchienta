## A class to describe weapons
#
class Weapon:

    def __init__( self, xmlElement ):
    
        # Set our name
        self.name = xmlElement.getAttribute("name")
    
        # Create a dictionary describing the weapon stats
        self.stats = {}
        statsElement = xmlElement.getElementsByTagName("stats")[0]
        for k in statsElement.attributes.keys():
            self.stats[k] = int(statsElement.attributes[k].value)

