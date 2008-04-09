import scene
import random

# forward definitions
class Warrior: pass

class Strategy:

    name = "Empty"
    description = "Empty strategy class."

    children = [Warrior]

    def __init__( self, m_battle, m_combatant ):

        self.sceneManager = scene.getSceneManager()

        self.m_combatant = m_combatant
        self.m_battle = m_battle
        self.turns = 0

    def control( self ):

        pass

class Warrior(Strategy):

    name = "Warrior"
    description = "Attacks enemies."

    children = []

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )

        self.turns = 3

    def control( self ):

        target = self.m_battle.activeCombatants[ random.randint(0,len(self.m_battle.activeCombatants)-1) ]
        self.sceneManager.info( self.m_combatant.name.capitalize()+" attacks "+target.name.capitalize() )
        self.turns -= 1

        self.m_combatant.delay += 6
