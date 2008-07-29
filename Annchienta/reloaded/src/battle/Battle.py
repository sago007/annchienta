import annchienta

## Holds a battle...
#
class Battle:

    def __init__( self, combatants ):
    
        # Set variables
        self.combatants = combatants
        
    def run( self ):
    
        while raw_input() is not 'q':
            self.update()
            self.draw()
        
    def update( self ):
    
        # Something with ms...
        pass
        
        # For now
        # take first combatant, have it attack and stick it up the back
        c = self.combatants.pop(0)
        action = c.selectAction()
        self.takeAction( action, c )
        self.combatants += [c]
        
    def draw( self ):
    
        # Text based for now
        print map( lambda a: a.name, self.combatants )

    ## Make an combatant do an action
    #
    def takeAction( self, action, combatant ):
        
        #Info
        target = self.combatants[ annchienta.randInt(0,len(self.combatants)-1) ]
        print combatant.name+" uses "+action.name+" on "+target.name+"!"
        
        # Let's assume we are dealing with a regular action for now
        baseDamage = 0.0
        if action.type == "physical":
            baseDamage = combatant.physicalBaseDamage()
        else:
            baseDamage = combatant.magicalBaseDamage()
            
        # Invert damage if we are dealing with restorative magic
        if action.elemental["restorative"]:
            baseDamage = -float(baseDamage)
            
        # Take the power of the attack into account
        baseDamage *= action.factor
        
        # Take the target's defense into account
        defense = target.derivedStats[ "def" if action.type == "physical" else "mdf" ]
        baseDamage *= ( (512.0 - target.derivedStats["def"])/512.0 )
    
        # Elemental properties now
        for element in action.elemental:
            if element != "restorative":
                # For example, if the action has "ice":1
                if action.elemental[element]:
                    # Multiply damage by the factor the
                    # target has set for it
                    baseDamage *= target.derivedElemental[element]
    
        print "The final damage is "+str(int(baseDamage))+"!"

