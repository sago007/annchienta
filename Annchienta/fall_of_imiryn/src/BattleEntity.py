import annchienta

# Class with very basic properties like
# attack, magic.. stats
class BattleEntity:

    ## Construct a BattleEntity from an xml element.
    #  this xml element should have the stats and
    #  elemental properties set.
    def __init__( self, xmlElement=None ):

        # Get a logmanager
        self.logManager = annchienta.getLogManager()

        # Every battleentity should have a name
        self.name = str( xmlElement.getAttribute("name") )

        # Create a dictionary describing the weapon stats
        self.stats = {}

        if xmlElement:
            statsElements = xmlElement.getElementsByTagName("stats")
            if len(statsElements):
                statsElement =  statsElements[0]
                for k in statsElement.attributes.keys():
                    self.stats[k] = int(statsElement.attributes[k].value)
            else:
                self.logManager.warning( "A BattleEntity should always define 'stats'." )

        # Create a dictionary describing the elemental properties
        self.elemental = {}

        if xmlElement:
            elementalElements = xmlElement.getElementsByTagName("elemental")
            if len(elementalElements):
                elementalElement = elementalElements[0]
                for k in elementalElement.attributes.keys():
                    self.elemental[k] = int(elementalElement.attributes[k].value)

    def getName( self ):
        return self.name
            
    def getAttack( self ):
        return self.stats["att"]

    def getDefense( self ):
        return self.stats["def"]

    def getMagicAttack( self ):
        return self.stats["mat"]

    def getMagicDefense( self ):
        return self.stats["mdf"]

    def getSpeed( self ):
        return self.stats["spd"]

    def getElementalFactor( self, element ):
        if element in self.elemental:
            return self.elemental[element]
        else:
            # Default...
            return 1.0

    def setElementalFactor( self, element, value ):
        self.elemental[element] = value
