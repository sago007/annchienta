## A class to describe weapons
#
class Weapon:

    def __init__( self, xmlElement ):
    
        # Set our name
        self.name = str(xmlElement.getAttribute("name"))
    
        # Create a dictionary describing the weapon stats
        self.stats = {}
        statsElement = xmlElement.getElementsByTagName("stats")[0]
        for k in statsElement.attributes.keys():
            self.stats[k] = int(statsElement.attributes[k].value)

        # Create a dictionary describing the elemental properties
        self.elemental = {}
        elementalElement = xmlElement.getElementsByTagName("elemental")[0]
        for k in elementalElement.attributes.keys():
            self.elemental[k] = int(elementalElement.attributes[k].value)
            
