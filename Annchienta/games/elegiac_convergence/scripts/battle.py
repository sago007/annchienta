import annchienta

class Combatant:

    videoManager = annchienta.getVideoManager()

    name = "Name"
    health = 6
    delay = 6
    hostile = False

    def __init__( self, name ):
        self.name = name

    def draw( self ):
        x = 40 if self.hostile else self.videoManager.getScreenWidth()-40-self.sprite.getWidth()
        self.videoManager.drawSurface( self.sprite, x, 40, self.sx1, self.sy1, self.sx2, self.sy2 )

    def setSprite( self, sprite, x1, y1, x2, y2 ):
        self.sprite = sprite
        self.sx1, self.sy1 = x1, y1
        self.sx2, self.sy2 = x2, y2

    def takeTurn( self ):
        self.delay += 6

class Ally(Combatant):
    pass

class Enemy(Combatant):
    pass

class Battle:

    videoManager = annchienta.getVideoManager()
    inputManager = annchienta.getInputManager()

    combatants = activeCombatants = []
    background = None
    running = False
    won = False

    def __init__( self, combatants ):
        self.activeCombatants = self.combatants = combatants
        self.running = True

    def run( self ):

        while self.running and self.inputManager.running():

            # For now
            self.inputManager.update()

            self.draw()

            # Find lowest delay.
            lowest = min( map( lambda c: c.delay, self.activeCombatants ) )

            # Subtract lowest from all delays.
            if lowest>0:
                for c in self.activeCombatants:
                    c.delay -= lowest

            # Select the first actor with delay 0.
            actors = filter( lambda c: c.delay<=0, self.activeCombatants )
            actor = actors[0]

            actor.takeTurn()

            # Update active combatants.
            self.activeCombatants = filter( lambda c: c.health>0, self.combatants )

            # Count enemies and allies.
            enemies = filter( lambda c: c.hostile, self.activeCombatants )
            allies = filter( lambda c: not c.hostile, self.activeCombatants )

            # Check for game over or victory
            if not len(enemies):
                self.onWin()
                return
            if not len(allies):
                self.onLose()
                return

    def draw( self ):

        self.videoManager.begin()

        for a in self.activeCombatants:
            a.draw()

        self.videoManager.end()

    def onWin( self ):
        self.won = True
        self.running = False
        print "You won!"

    def onLose( self ):
        self.won = False
        self.running = False
        print "You lost..."
