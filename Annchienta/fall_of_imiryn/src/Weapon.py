import BattleEntity

## A class to describe weapons
#
class Weapon( BattleEntity.BattleEntity ):

    def __init__( self, xmlElement ):

        # Call super constructor.
        BattleEntity.BattleEntity.__init__( self, xmlElement )
    
        # Set our name
        self.description = str(xmlElement.getAttribute("description"))
    
    def getDescription( self ):
        return self.description
