import xml.dom.minidom
import annchienta
import combatant
import scene
import party

class Battle:

    combatants = activeCombatants = []
    background = None
    running = False
    won = False

    def __init__( self, combatants ):

        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.mapManager = annchienta.getMapManager()
        self.audioManager = annchienta.getAudioManager()
        self.cacheManager = annchienta.getCacheManager()
        self.mathManager = annchienta.getMathManager()
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
            a.setPosition( self.videoManager.getScreenWidth()/2-30-i*10-w, 100+i*40-h )

        for i in range( len(self.enemies) ):
            e = self.enemies[i]
            w, h = e.getSize()
            e.setPosition( self.videoManager.getScreenWidth()/2+30+i*10, 100+i*40-h )

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

        self.draw()

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

            # Perform dying animations.
            for a in self.activeCombatants:
                if a.status.get("health")<=0:
                    self.dieAnimation(a)

            self.updateCombatantArrays()

            # Check for game over or victory
            if not len(self.enemies) or self.inputManager.keyDown(annchienta.SDLK_a):
                self.onWin()
                return
            if not len(self.allies):
                self.onLose()
                return

    def draw( self, flip=True ):

        self.videoManager.clear()

        # Draw the background
        if self.background is not None:
            self.videoManager.drawSurface( self.background, 0, 0 )

        # Sort the combatants on depth.
            self.activeCombatants.sort( lambda c1, c2: c1.y-c2.y )

        for a in self.activeCombatants:

            self.videoManager.reset()
            a.draw()

            # Draw some basic info
            x, y = a.posX, a.posY
            w, h = a.getSize()
            x += (w+5 if a.hostile else -5-64)
            y += (h - 50)
            self.sceneManager.drawBox( x, y, x+64, y+30 )
            self.videoManager.translate( x, y )

            # Health bar.
            self.videoManager.setColor(0,0,0)
            self.videoManager.drawRectangle( 5, 5, 59, 10 )
            self.videoManager.setColor(200,0,0)
            w = int(54.0*float(a.status.get("health"))/float(a.status.get("maxhealth")))
            self.videoManager.drawRectangle( 5, 5, 5+w, 10 )

            # Ailments and buffers.
            self.videoManager.translate( 0, 10 )
            self.videoManager.setColor()
            for effect in a.ailments+a.buffers:
                surf = self.cacheManager.getSurface("images/status_effects/"+effect+".png")
                self.videoManager.drawSurface( surf, 0, 0 )
                self.videoManager.translate( surf.getWidth(), 0 )

        self.videoManager.reset()
        if flip:
            self.videoManager.flip()

    def onWin( self ):
        self.won = True
        self.running = False
        self.sceneManager.info( "Victory!", None )
        experienceGaining = filter( lambda a: a.status.get("health")>0, self.allies )
        points = sum( map(lambda e: e.experience, filter( lambda c: c.hostile, self.combatants) ) )
        for e in experienceGaining:
            e.addGrowthPoints( points )
        # Give some health.
        for a in filter( lambda c: not c.hostile, self.combatants ):
            a.addHealth( int(0.2*float(a.status.get("maxhealth"))) )

    def onLose( self ):
        self.won = False
        self.running = False

        self.audioManager.playMusic( "music/game_over.ogg" )

        # Little animation
        s = annchienta.Surface( "images/animations/game_over.png" )
        self.videoManager.drawSurface( s, 0, 0 )
        self.sceneManager.fadeOut( 100, 0, 0, 5000 )
        self.sceneManager.waitForClick()

        #self.sceneManager.info( "You lost...", None )
        self.mapManager.stop()

    def getCombatantWithLowestHealth( self, hostile ):
        array = self.enemies if hostile else self.allies
        if not len(array):
            return None
        comb = array[0]
        for a in array[1:]:
            if a.status.get("health")<comb.status.get("health"):
                comb = a
        return comb

    def moveAnimation( self, mover, tx, ty, duration=300 ):
        ox, oy = mover.x, mover.y
        start = self.engine.getTicks()
        while self.engine.getTicks()<start+duration and self.inputManager.running():
            t = float(self.engine.getTicks()-start)/float(duration)
            mover.x = int( t*float(tx) + (1.0-t)*float(ox) )
            mover.y = int( t*float(ty) + (1.0-t)*float(oy ) )
            self.draw()
            self.engine.delay(1)

    def physicalAttackAnimation( self, attacker, target ):

        tw, th = target.getSize()
        aw, ah = attacker.getSize()
        tx = target.x-aw if target.hostile else target.x+tw
        ty = target.y+th-ah

        self.moveAnimation( attacker, tx, ty )

    def returnHomeAnimation( self, mover ):

        self.moveAnimation( mover, mover.posX, mover.posY )

    def surfaceOverSpritesAnimation( self, targets, surface, rtx, rty, duration=300, backwards=False ):

        sizes = map( lambda t: t.getSize(), targets )
        ox = map( lambda i: targets[i].x+sizes[i][0]/2-surface.getWidth()/2, range(len(targets)) )
        oy = map( lambda i: targets[i].y+sizes[i][1]/2-surface.getHeight()/2, range(len(targets)) )
        tx = map( lambda i: ox[i]+rtx, range(len(targets)) )
        ty = map( lambda i: oy[i]+rty, range(len(targets)) )
        start = self.engine.getTicks()

        while self.engine.getTicks()<start+duration and self.inputManager.running():
            t = float(self.engine.getTicks()-start)/float(duration)
            t = 1.0-t if backwards else t
            self.draw(False)
            for i in range(len(targets)):
                x = int( t*float(tx[i]) + (1.0-t)*float(ox[i]) )
                y = int( t*float(ty[i]) + (1.0-t)*float(oy[i]) )
                self.videoManager.drawSurface( surface, x, y )
            self.videoManager.flip()
            self.engine.delay(1)

    def dieAnimation( self, actor ):

        self.moveAnimation( actor, actor.x + (20 if actor.hostile else -20), actor.y )
        self.activeCombatants = filter( lambda a: a is not actor, self.activeCombatants )
        self.draw()

class BattleManager:

    enemyElements = []
    m_battle = None

    def __init__( self ):
        
        self.audioManager = annchienta.getAudioManager()
        self.mathManager = annchienta.getMathManager()
        self.logManager = annchienta.getLogManager()
        self.engine = annchienta.getEngine()
    
        self.enemiesInMap = []
        self.battleBackground = None
        self.randomBattleDelay = self.mathManager.randInt( 300, 1000 )

    def loadEnemies( self, fname ):

        self.document = xml.dom.minidom.parse( fname )
        self.enemyElements = self.document.getElementsByTagName("combatant")

    def createEnemy( self, name ):

        candidates = filter( lambda e: str(e.getAttribute("name")).lower()==name.lower(), self.enemyElements )
        if not len(candidates):
            self.logManager.error( "Could not find an enemy called '"+str(name)+"'." )
        else:
            return combatant.Enemy( candidates[0] )

    def throwRandomBattle( self ):

        self.partyManager = party.getPartyManager()
        self.sceneManager = scene.getSceneManager()

        if self.randomBattleDelay>0:
            self.randomBattleDelay -= 1
            return
        else:
            self.randomBattleDelay = self.mathManager.randInt( 300, 1000 )

            # Return if there are no enemies in this level.
            if not len(self.enemiesInMap):
                return

            music = self.audioManager.getPlayingMusic()
            self.audioManager.playMusic( "music/battle_"+str(self.mathManager.randInt(1,4))+".ogg" )
            self.sceneManager.rotateEffect()

            enames = map( lambda a: self.enemiesInMap[self.mathManager.randInt(0,len(self.enemiesInMap))], range(self.mathManager.randInt(2,4)))
            enemies = map( lambda n: self.createEnemy(n), enames )

            b = Battle( self.partyManager.team + enemies )
            b.background = annchienta.Surface(self.battleBackground)
            b.run()

            self.audioManager.playMusic( music )

def initBattleManager():
    global globalBattleManagerInstance
    globalBattleManagerInstance = BattleManager()

def getBattleManager():
    return globalBattleManagerInstance
