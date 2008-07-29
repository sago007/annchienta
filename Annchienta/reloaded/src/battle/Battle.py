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
        print c.name+" acts!"
        self.combatants += [c]
        
    def draw( self ):
    
        # Text based for now
        print map( lambda a: a.name, self.combatants )

