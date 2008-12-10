import annchienta
import Combatant

class Enemy( Combatant.Combatant ):

    def __init__( self, xmlElement ):
        
        # Base constructor
        Combatant.Combatant.__init__( self, xmlElement )
        
        # We need a drop element for enemies
        dropElement = xmlElement.getElementsByTagName("drop")[0]
        self.dropXp = int( dropElement.getAttribute("xp") )
        if dropElement.hasAttribute("item"):
            self.dropItem = str( dropElement.getAttribute("item") )
            self.dropRate = float( dropElement.getAttribute("rate") )
        else:
            self.dropItem = None
        if dropElement.hasAttribute("steal"):
            self.stealableItem = str( dropElement.getAttribute("steal") )
        else:
            self.stealableItem = None

    def isAlly( self ):
        return False

    def getDropXp( self ):
        return self.dropXp

    def getDropItem( self ):
        return self.dropItem

    def getDropRate( self ):
        return self.dropRate

    def getStealableItem( self ):
        return self.stealableItem

    def stealItem( self ):
        self.stealableItem = None

    # Enemies perform a random action for now
    def selectAction( self, battle ):
    
        # Select an action
        actions = filter( lambda a: a.getCost() <= self.getMp(), self.actions )
        action = self.actions[ self.mathManager.randInt( 0, len(self.actions) ) ]

        # Select a target
        target = self.selectTarget( battle )

        return action, target

    def selectTarget( self, battle ):
        return battle.allies[ self.mathManager.randInt( 0, len(battle.allies) ) ]
