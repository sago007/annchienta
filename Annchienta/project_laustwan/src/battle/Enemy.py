import annchienta
import Combatant

class Enemy( Combatant.Combatant ):

    def __init__( self, xmlElement ):
        
        # Base constructor
        Combatant.Combatant.__init__( self, xmlElement )
        
        # Variables
        self.ally = False

        # We need a drop element for enemies
        dropElement = xmlElement.getElementsByTagName("drop")[0]
        self.dropXp = int( dropElement.getAttribute("xp") )
        if dropElement.hasAttribute("item"):
            self.dropItem = str( dropElement.getAttribute("item") )
            self.dropRate = float( dropElement.getAttribute("rate") )
        else:
            self.dropItem = None
        if dropElement.hasAttribute("steal"):
            self.steal = str( dropElement.getAttribute("steal") )
        else:
            self.steal = None

    # Enemies perform a random action for now
    def selectAction( self, battle ):
    
        # Select an action
        actions = filter( lambda a: a.cost <= self.healthStats["mp"], self.actions )
        action = self.actions[ annchienta.randInt( 0, len(self.actions)-1 ) ]

        # Select a target
        target = self.selectTarget( battle )

        return action, target

    def selectTarget( self, battle ):
        return battle.allies[ annchienta.randInt( 0, len(battle.allies)-1 ) ]

