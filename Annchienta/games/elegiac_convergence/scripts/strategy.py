import annchienta
import scene

## STRATEGY GUIDELINES
#
#  strength+defense+magic+resistance == 10
#
#  a strategy should do 5 standard damage per 1 delay
#  or heal 1/28 per 1 delay
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
        target = array[ annchienta.randInt(0,len(array)-1) ]

        # Attack that target with default attack power (=30).
        self.sceneManager.info( self.m_combatant.name.capitalize()+" attacks "+target.name.capitalize()+"!" )
        self.m_battle.physicalAttackAnimation( self.m_combatant, target )
        sound = self.cacheManager.getSound("sounds/sword.ogg")
        if self.m_combatant.physicalAttack( target, 30, 0.8 ):
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

        # Attack all targets with 20 attack power.
        self.sceneManager.info( self.m_combatant.name.capitalize()+" casts ice!" )
        surf = self.cacheManager.getSurface("images/animations/ice.png")
        sound = self.cacheManager.getSound("sounds/ice.ogg")
        self.audioManager.playSound( sound )
        self.m_battle.surfaceOverSpritesAnimation( array, surf, -50 if self.m_combatant.hostile else 50, 0 )
        for e in array:
            self.m_combatant.magicalAttack( e, 20, 0.7 )

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
        self.m_combatant.delay += 6

        # Select the target with the lowest health.
        target = self.m_battle.getCombatantWithLowestHealth( not self.m_combatant.hostile )
        if target is None:
            return

        # Attack that target with some more attack power.
        self.sceneManager.info( self.m_combatant.name.capitalize()+" attacks "+target.name.capitalize()+"!" )
        self.m_battle.physicalAttackAnimation( self.m_combatant, target )
        sound = self.cacheManager.getSound("sounds/sword.ogg")
        if self.m_combatant.physicalAttack( target, 30, 0.7 ):
            self.audioManager.playSound( sound )
        self.m_battle.returnHomeAnimation( self.m_combatant )

    def isAvailableFor( self, m_combatant ):
        return m_combatant.experience.get("warrior")>6

## MONK
#
#  A white-magic based class that protects other fighters.
#
class Monk(Strategy):

    name = "monk"
    description = "Supports allies."
    strength, defense, magic, resistance = 1, 4, 1, 4

    category = "white magic"

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )
        self.turns = 2

    def control( self ):

        # Decrease our turns for this strategy.
        self.turns -= 1

        # Add some delay now.
        self.m_combatant.delay += 6

        # Select first array.
        array = self.m_battle.enemies if self.m_combatant.hostile else self.m_battle.allies
        # Filter based on status effects.
        array = filter( lambda c: not ("protect" in c.buffers and "barrier" in c.buffers), array )
        if not len(array):
            return

        target = array[ annchienta.randInt(0,len(array)-1) ]

        status = ""
        if "protect" in target.buffers:
            status = "barrier"
        elif "barrier" in target.buffers:
            status = "protect"
        else:
            status = "protect" if annchienta.randInt(0,1) else "barrier"

        # Add that status effect.
        if status=="protect":
            self.sceneManager.info( self.m_combatant.name.capitalize()+" creates a protection arround "+target.name.capitalize()+"!" )
        else:
            self.sceneManager.info( self.m_combatant.name.capitalize()+" creates a barrier for "+target.name.capitalize()+"!" )

        target.buffers += [status]

    def isAvailableFor( self, m_combatant ):
        return m_combatant.experience.get("healer")>6

## ADEPT
#
#  Most simple black-magic based class. Casts a spell on
#  all opponents.
#
class Poisoner(Strategy):

    name = "poisoner"
    description = "Tries to poison enemies."
    strength, defense, magic, resistance = 1, 3, 4, 2

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
        if not len(array):
            return
        target = array[ annchienta.randInt(0,len(array)-1) ]

        # Attack all targets with 12 attack power.
        self.sceneManager.info( self.m_combatant.name.capitalize()+" casts bio on "+target.name.capitalize()+"!" )
        surf = self.cacheManager.getSurface("images/animations/poison.png")
        sound = self.cacheManager.getSound("sounds/poison.ogg")
        self.audioManager.playSound( sound )
        self.m_battle.surfaceOverSpritesAnimation( [target], surf, -50 if self.m_combatant.hostile else 50, 0 )
        self.m_combatant.magicalAttack( target, 20, 0.7 )
        if not "poison" in target.ailments:
            target.ailments += ["poison"]

    def isAvailableFor( self, m_combatant ):
        return m_combatant.experience.get("adept")>6

## DRAGON
#
#  A melee-based class only available for Inyse. Attacks a
#  random target with some serious power.
#
class Dragon(Strategy):

    name = "dragon"
    description = "Randomly brutally attacks enemies."
    strength, defense, magic, resistance = 4, 2, 1, 3

    category = "melee"

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )
        self.turns = 3

    def control( self ):

        # Decrease our turns for this strategy.
        self.turns -= 1

        # Add some delay now. Quite much delay, since we're doing a lot of damage.
        self.m_combatant.delay += 9

        # Select any random target.
        array = self.m_battle.allies if self.m_combatant.hostile else self.m_battle.enemies
        if not len(array):
            return
        target = array[ annchienta.randInt(0,len(array)-1) ]

        # Attack that target with serious attack power (=50).
        self.sceneManager.info( self.m_combatant.name.capitalize()+" attacks "+target.name.capitalize()+"!" )
        # A jump in the air first.
        self.m_battle.moveAnimation( self.m_combatant, self.m_combatant.x + (-10 if self.m_combatant.hostile else 10 ), self.m_combatant.y-200 )
        self.m_battle.physicalAttackAnimation( self.m_combatant, target )
        sound = self.cacheManager.getSound("sounds/sword.ogg")
        if self.m_combatant.physicalAttack( target, 50, 0.8 ):
            self.audioManager.playSound( sound )
        self.m_battle.returnHomeAnimation( self.m_combatant )

    def isAvailableFor( self, m_combatant ):
        return False

## LICH
#
#  Simple black-magic based class which is also used by
#  ghosts etc.
#
class Lich(Strategy):

    name = "lich"
    description = "Dark arcane arts."
    strength, defense, magic, resistance = 1, 3, 3, 3

    category = "black magic"

    def __init__( self, m_battle, m_combatant ):

        Strategy.__init__( self, m_battle, m_combatant )
        self.turns = 3

    def control( self ):

        # Decrease our turns for this strategy.
        self.turns -= 1

        # Add some delay now.
        self.m_combatant.delay += 6

        # Select all targets
        array = self.m_battle.allies if self.m_combatant.hostile else self.m_battle.enemies

        # Attack all targets with 24 attack power.
        self.sceneManager.info( self.m_combatant.name.capitalize()+" casts bleed!" )
        surf = self.cacheManager.getSurface("images/animations/bleed.png")
        sound = self.cacheManager.getSound("sounds/bleed.ogg")
        self.audioManager.playSound( sound )
        self.m_battle.surfaceOverSpritesAnimation( array, surf, -50 if self.m_combatant.hostile else 50, 0 )
        for e in array:
            self.m_combatant.magicalAttack( e, 25, 0.7 )

    def isAvailableFor( self, m_combatant ):
        return False

# List with all strategies, used by getStrategy()
all = [Warrior, Healer, Adept, Fighter, Monk, Poisoner, Dragon, Lich]

def getStrategy( name ):
    for s in all:
        if s.name.lower() == name.lower():
            return s
    return Strategy
