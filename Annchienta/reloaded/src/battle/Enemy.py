import annchienta
import Combatant

class Enemy( Combatant.Combatant ):

    def __init__( self, xmlElement ):
        
        # Base constructor
        Combatant.Combatant.__init__( self, xmlElement )
        
        # Variables
        self.ally = False

    # Enemies perform a random action for now
    def selectAction( self, battle ):
    
        # Select an action
        actions = filter( lambda a: a.cost <= self.healthStats["mp"], self.actions )
        action = self.actions[ annchienta.randInt( 0, len(self.actions)-1 ) ]

        # Select a target
        target = self.selectTarget( battle )

        return action, target

    def selectTarget( self, battle ):
        return battle.combatants[ annchienta.randInt( 0, len(battle.combatants)-1 ) ]
