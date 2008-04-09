import scene
import random

class Strategy:

    name = "empty"
    description = "Empty strategy class."

    children = ["warrior","healer"]

    def __init__( self, m_battle, m_combatant ):

        self.sceneManager = scene.getSceneManager()

        self.m_combatant = m_combatant
        self.m_battle = m_battle
        self.turns = 0

    def control( self ):

        pass

class Warrior(Strategy):

    name = "warrior"
    description = "Attacks enemies."

    children = ["ninja", "defender"]

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )

        self.turns = 3

    def control( self ):

        target = self.m_battle.activeCombatants[ random.randint(0,len(self.m_battle.activeCombatants)-1) ]
        self.sceneManager.info( self.m_combatant.name.capitalize()+" attacks "+target.name.capitalize()+" ("+str(self.turns)+")" )
        self.turns -= 1

        self.m_combatant.delay += 6

class Healer(Strategy):

    name = "healer"
    description = "Heals allies"

    children = []

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )

        self.turns = 3

    def control( self ):

        target = self.m_battle.activeCombatants[ random.randint(0,len(self.m_battle.activeCombatants)-1) ]
        self.sceneManager.info( self.m_combatant.name.capitalize()+" heals "+target.name.capitalize()+" ("+str(self.turns)+")" )
        self.turns -= 1

        self.m_combatant.delay += 6

class Ninja(Strategy):

    name = "ninja"
    description = "Does what ninja's do."

    children = []

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )

        self.turns = 3

    def control( self ):

        target = self.m_battle.activeCombatants[ random.randint(0,len(self.m_battle.activeCombatants)-1) ]
        self.sceneManager.info( self.m_combatant.name.capitalize()+" ninja-attacks "+target.name.capitalize()+" ("+str(self.turns)+")" )
        self.turns -= 1

        self.m_combatant.delay += 6

class Defender(Strategy):

    name = "defender"
    description = "Defends around."

    children = []

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )

        self.turns = 3

    def control( self ):

        target = self.m_battle.activeCombatants[ random.randint(0,len(self.m_battle.activeCombatants)-1) ]
        self.sceneManager.info( self.m_combatant.name.capitalize()+" defends. ("+str(self.turns)+")" )
        self.turns -= 1

        self.m_combatant.delay += 6

# List with all strategies, used by getStrategy()
all = [Warrior, Healer, Ninja, Defender]

def getStrategy( name ):
    for s in all:
        if s.name.lower() == name.lower():
            return s
    return Strategy
