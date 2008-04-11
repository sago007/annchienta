import scene
import random

class Strategy:

    name = "empty"
    description = "Empty strategy class."

    def __init__( self, m_battle, m_combatant ):

        self.sceneManager = scene.getSceneManager()

        self.m_combatant = m_combatant
        self.m_battle = m_battle
        self.turns = 0

    def control( self ):

        pass

    # Note that this does not take a 'self' parameter,
    # meaning you should call it like 'Strategy.isAvailableFor()'
    def isAvailableFor( m_combatant ):

        return True

## WARRIOR
#
#  Most simple melee-based class. Selects a random target
#  every turn and performs a regular attack on that target.
#
class Warrior(Strategy):

    name = "warrior"
    description = "Attacks enemies."

    category = "melee"

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )

        self.turns = 3

    def control( self ):

        # Decrease our turns for this strategy.
        self.turns -= 1

        # Add some delay now.
        self.m_combatant.delay += 6

        # Select any random target.
        array = self.m_battle.allies if self.m_combatant.hostile else self.m_battle.enemies
        if not len(array):
            return
        target = array[ random.randint(0,len(array)-1) ]

        # Attack that target with default attack power (=20).
        self.sceneManager.info( self.m_combatant.name.capitalize()+" attacks "+target.name.capitalize()+"!" )
        self.m_battle.physicalAttackAnimation( self.m_combatant, target )
        self.m_combatant.physicalAttack( target, 20, 0.8 )


## HEALER
#
#  Most simple white-magic based class. Selects the ally
#  with the lowest health and performs a simple cure on
#  that ally.
#
class Healer(Strategy):

    name = "healer"
    description = "Heals allies"

    category = "white magic"

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )

        self.turns = 3

    def control( self ):

        target = self.m_battle.activeCombatants[ random.randint(0,len(self.m_battle.activeCombatants)-1) ]
        self.sceneManager.info( self.m_combatant.name.capitalize()+" heals "+target.name.capitalize()+" ("+str(self.turns)+")" )
        self.turns -= 1

        self.m_combatant.delay += 6

# List with all strategies, used by getStrategy()
all = [Warrior, Healer]

def getStrategy( name ):
    for s in all:
        if s.name.lower() == name.lower():
            return s
    return Strategy
