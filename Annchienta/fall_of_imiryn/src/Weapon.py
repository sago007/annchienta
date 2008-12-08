import BattleEntity

## A class to describe weapons
#
class Weapon( BattleEntity.BattleEntity ):

    def __init__( self, xmlElement ):

        # Call super constructor.
        BattleEntity.BattleEntity.__init__( self, xmlElement )
    
        # Set our name
        self.name = str(xmlElement.getAttribute("name"))
        self.description = str(xmlElement.getAttribute("description"))
    
    def getName( self ):
        return self.name

    def getDescription( self ):
        return self.description
