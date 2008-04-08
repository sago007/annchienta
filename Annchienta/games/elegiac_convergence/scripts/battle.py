import xml.dom.minidom
import annchienta
import combatant
import scene

class Battle:

    videoManager = annchienta.getVideoManager()
    inputManager = annchienta.getInputManager()
    sceneManager = scene.getSceneManager()

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
            # self.inputManager.update()

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

            # Let that actor take a turn. This will increase
            # it's delay as well.
            actor.takeTurn()

            # Update active combatants.
            self.activeCombatants = filter( lambda c: c.health>0, self.combatants )

            # Count enemies and allies.
            enemies = filter( lambda c: c.hostile, self.activeCombatants )
            allies = filter( lambda c: not c.hostile, self.activeCombatants )

            # Check for game over or victory
            if not len(enemies) or self.inputManager.keyDown(annchienta.SDLK_a):
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
        self.sceneManager.info( "You won!" )

    def onLose( self ):
        self.won = False
        self.running = False
        self.sceneManager.info( "You lost..." )


class BattleManager:

    engine = annchienta.getEngine()

    enemyElements = []

    def loadEnemies( self, fname ):

        self.document = xml.dom.minidom.parse( fname )
        self.enemyElements = self.document.getElementsByTagName("combatant")

    def createEnemy( self, name ):

        candidates = filter( lambda e: str(e.getAttribute("name")).lower()==name.lower(), self.enemyElements )
        if not len(candidates):
            self.engine.write( "Error - could not find an enemy called "+str(name)+"." )
        else:
            return combatant.Enemy( candidates[0] )

def initBattleManager():
    global globalBattleManagerInstance
    globalBattleManagerInstance = BattleManager()

def getBattleManager():
    return globalBattleManagerInstance
