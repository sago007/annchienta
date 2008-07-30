import Combatant

class Ally( Combatant.Combatant ):

    def __init__( self, xmlElement ):
        
        # Base constructor
        Combatant.Combatant.__init__( self, xmlElement )
        
        # Variables
        self.ally = True

    # Allies select an action from the menu
    def selectAction( self, battle ):
    
        
        return self.actions[ annchienta.randInt( 0, len(self.actions)-1 ) ]
        
