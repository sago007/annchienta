import annchienta
import scene
import random

class Strategy:

    name = "empty"
    description = "Empty strategy class."
    strength, defense, magic, resistance = 3, 2, 3, 2

    def __init__( self, m_battle, m_combatant ):

        self.cacheManager = annchienta.getCacheManager()
        self.audioManager = annchienta.getAudioManager()
        self.sceneManager = scene.getSceneManager()

        self.m_combatant = m_combatant
        self.m_battle = m_battle
        self.turns = 0

    def control( self ):

        pass

    def isAvailableFor( self, m_combatant ):
        return True

## WARRIOR
#
#  Most simple melee-based class. Selects a random target
#  every turn and performs a regular attack on that target.
#
class Warrior(Strategy):

    name = "warrior"
    description = "Randomly attacks enemies."
    strength, defense, magic, resistance = 4, 3, 1, 2

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
        sound = self.cacheManager.getSound("sounds/sword.ogg")
        if self.m_combatant.physicalAttack( target, 20, 0.8 ):
            self.audioManager.playSound( sound )
        self.m_battle.returnHomeAnimation( self.m_combatant )

    def isAvailableFor( self, m_combatant ):
        return True

## HEALER
#
#  Most simple white-magic based class. Selects the ally
#  with the lowest health and performs a simple cure on
#  that ally.
#
class Healer(Strategy):

    name = "healer"
    description = "Heals allies."
    strength, defense, magic, resistance = 1, 2, 3, 4

    category = "white magic"

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )
        self.turns = 3

    def control( self ):

        # Decrease our turns for this strategy.
        self.turns -= 1

        # Add some delay now.
        self.m_combatant.delay += 7

        # Select the allie with the lowest health.
        target = self.m_battle.getCombatantWithLowestHealth( self.m_combatant.hostile )
        if target is None:
            return

        # Heal that target for 1/4 of his health.
        self.sceneManager.info( self.m_combatant.name.capitalize()+" heals "+target.name.capitalize()+"!" )
        target.addHealth( target.status.get("maxhealth")/4 )
        surf = self.cacheManager.getSurface("images/animations/cure.png")
        sound = self.cacheManager.getSound("sounds/cure.ogg")
        self.audioManager.playSound( sound )
        self.m_battle.surfaceOverSpritesAnimation( [target], surf, 0, -50 )

    def isAvailableFor( self, m_combatant ):
        return True

## ADEPT
#
#  Most simple black-magic based class. Casts a spell on
#  all opponents.
#
class Adept(Strategy):

    name = "adept"
    description = "Casts spells on enemies."
    strength, defense, magic, resistance = 1, 2, 4, 3

    category = "black magic"

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

        # Attack all targets with 10 attack power.
        self.sceneManager.info( self.m_combatant.name.capitalize()+" casts ice!" )
        surf = self.cacheManager.getSurface("images/animations/ice.png")
        sound = self.cacheManager.getSound("sounds/ice.ogg")
        self.audioManager.playSound( sound )
        self.m_battle.surfaceOverSpritesAnimation( array, surf, -50 if self.m_combatant.hostile else 50, 0 )
        for e in array:
            self.m_combatant.magicalAttack( e, 10, 0.7 )

    def isAvailableFor( self, m_combatant ):
        return True

## FIGHTER
#
#  Attacks the weakest enemies.
#
class Fighter(Strategy):

    name = "fighter"
    description = "Attacks the weakest enemy."
    strength, defense, magic, resistance = 4, 4, 1, 1

    category = "melee"

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )
        self.turns = 3

    def control( self ):

        # Decrease our turns for this strategy.
        self.turns -= 1

        # Add some delay now.
        self.m_combatant.delay += 7

        # Select the target with the lowest health.
        target = self.m_battle.getCombatantWithLowestHealth( not self.m_combatant.hostile )
        if target is None:
            return

        # Attack that target with some more attack power.
        self.sceneManager.info( self.m_combatant.name.capitalize()+" attacks "+target.name.capitalize()+"!" )
        self.m_battle.physicalAttackAnimation( self.m_combatant, target )
        sound = self.cacheManager.getSound("sounds/sword.ogg")
        if self.m_combatant.physicalAttack( target, 25, 0.8 ):
            self.audioManager.playSound( sound )
        self.m_battle.returnHomeAnimation( self.m_combatant )

    def isAvailableFor( self, m_combatant ):
        return m_combatant.experience.get("warrior")>2

# List with all strategies, used by getStrategy()
all = [Warrior, Healer, Adept, Fighter]

def getStrategy( name ):
    for s in all:
        if s.name.lower() == name.lower():
            return s
    return Strategy
