import xml.dom.minidom
import annchienta
import combatant
import scene

class Battle:

    videoManager = annchienta.getVideoManager()
    inputManager = annchienta.getInputManager()
    mapManager = annchienta.getMapManager()
    engine = annchienta.getEngine()

    combatants = activeCombatants = []
    background = None
    running = False
    won = False

    def __init__( self, combatants ):

        self.sceneManager = scene.getSceneManager()
        self.battleManager = getBattleManager()
        
        self.activeCombatants = self.combatants = combatants
        self.running = True

        self.enemies = filter( lambda c: c.hostile, self.activeCombatants )
        self.allies = filter( lambda c: not c.hostile, self.activeCombatants )

        # Set positions for combatants
        for i in range( len(self.allies) ):
            a = self.allies[i]
            w, h = a.getSize()
            a.setPosition( self.videoManager.getScreenWidth()/2-30-i*20-w, 100+i*40-h )

        for i in range( len(self.enemies) ):
            e = self.enemies[i]
            w, h = e.getSize()
            e.setPosition( self.videoManager.getScreenWidth()/2+30+i*20, 100+i*40-h )

        self.updateCombatantArrays()

        self.background = None

    def updateCombatantArrays( self ):
        # Update active combatants.
        self.activeCombatants = filter( lambda c: c.status.get("health")>0, self.combatants )

        # Count enemies and allies.
        self.enemies = filter( lambda c: c.hostile, self.activeCombatants )
        self.allies = filter( lambda c: not c.hostile, self.activeCombatants )

    def run( self ):

        self.battleManager.m_battle = self

        for a in self.combatants:
            a.reset()
            a.m_battle = self

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

            self.draw()

            if not self.inputManager.running():
                return

            self.updateCombatantArrays()

            # Check for game over or victory
            if not len(self.enemies) or self.inputManager.keyDown(annchienta.SDLK_a):
                self.onWin()
                return
            if not len(self.allies):
                self.onLose()
                return

    def draw( self, flip=True ):

        self.videoManager.begin()

        # Draw the background
        if self.background is not None:
            self.videoManager.drawSurface( self.background, 0, 0 )

        # Sort them before drawing
        self.activeCombatants.sort( lambda c1, c2: c1.y-c2.y )

        for a in self.activeCombatants:

            self.videoManager.reset()
            a.draw()

            # Draw some basic info
            x, y = a.posX, a.posY
            w, h = a.getSize()
            x += (w+20 if a.hostile else -20-60)
            y += (h - 50)
            self.videoManager.translate( x, y )
            self.sceneManager.drawBox( 0, 0, 60, 30 )

            # Health bar.
            self.videoManager.setColor(0,0,0)
            self.videoManager.drawRectangle( 5, 5, 55, 10 )
            self.videoManager.setColor(200,0,0)
            w = int(50.0*float(a.status.get("health"))/float(a.status.get("maxhealth")))
            self.videoManager.drawRectangle( 5, 5, 5+w, 10 )

            self.sceneManager.inactiveColor()
            # Ailments and buffers.
            if not (len(a.ailments)+len(a.buffers)):
                self.videoManager.drawString( self.sceneManager.defaultFont, "Clean", 5, 10 )

        if flip:
            self.videoManager.end()

    def onWin( self ):
        self.won = True
        self.running = False
        self.sceneManager.info( "You won!", None )

    def onLose( self ):
        self.won = False
        self.running = False
        self.sceneManager.info( "You lost...", None )
        self.mapManager.stop()

    def getCombatantWithLowestHealth( self, hostile ):
        array = self.enemies if hostile else self.allies
        comb = array[0]
        for a in array[1:]:
            if a.status.get("health")<comb.status.get("health"):
                comb = a
        return comb

    def physicalAttackAnimation( self, attacker, target ):
        duration = 600
        start = self.engine.getTicks()

        tw, th = target.getSize()
        aw, ah = attacker.getSize()
        tx = target.x-aw if target.hostile else target.x+tw
        ty = target.y+th-ah

        while self.engine.getTicks()<start+duration:
            t = float(self.engine.getTicks()-start)/float(duration)
            attacker.x = int( t*float(tx) + (1.0-t)*float(attacker.posX) )
            attacker.y = int( t*float(ty) + (1.0-t)*float(attacker.posY) )
            self.draw()

        attacker.x, attacker.y = attacker.posX, attacker.posY

class BattleManager:

    engine = annchienta.getEngine()

    enemyElements = []
    m_battle = None

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
