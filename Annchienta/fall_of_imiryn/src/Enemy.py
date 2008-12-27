import annchienta
from Combatant import Combatant
from Action import Action

class Enemy( Combatant ):

    def __init__( self, xmlElement ):
        
        # Base constructor
        Combatant.__init__( self, xmlElement )
        
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

        # Might move to front row when in the back
        if self.getRow() is "back":
            rowAction = Action()
            rowAction.name = "row"
            rowAction.category = "top"
            rowAction.target = 0
            actions += [rowAction]

        action = actions[ self.mathManager.randInt( 0, len(actions) ) ]

        # Select a target
        target = None
        if action.hasTarget():
            target = self.selectTarget( battle )

        return action, target

    def selectTarget( self, battle ):
        return battle.allies[ self.mathManager.randInt( 0, len(battle.allies) ) ]
