import annchienta
import PartyManager, SceneManager

class GameObject:

    def __init__( self, position, sprite ):

        self.videoManager = annchienta.getVideoManager()
        self.pos = position
        self.sprite = sprite
        self.dir = annchienta.Vector( 0, 0 )

    def draw( self ):

        self.videoManager.push()
        self.videoManager.translate( self.pos.x, self.pos.y )
        self.videoManager.drawSurface( self.sprite, -self.sprite.getWidth()/2, -self.sprite.getHeight()/2 )
        self.videoManager.pop()

class Game:

    def __init__( self ):

        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.cacheManager = annchienta.getCacheManager()
        self.mapManager   = annchienta.getMapManager()
        self.mathManager  = annchienta.getMathManager()
        self.sceneManager = SceneManager.getSceneManager()

        # Background spriteace
        self.background = annchienta.Surface( "images/backgrounds/sky.png" )
        self.backgroundY = 0.0

        # Create a ship for the player
        self.ship = GameObject( annchienta.Vector( videoManager.getScreenWidth()/2, videoManager.getScreenHeight()/2 ),
                                annchienta.Surface( "sprites/ship_small.png" ) )

        # Load sprites into cache
        self.enemySprite = annchienta.Surface("sprites/ship_pirate.png")

        # All enemies
        self.enemies = []

        # The final enemy
        self.captain = None

        # Number of miliseconds we need to fly to gain victory
        self.victoryTime = 60000

    def run( self ):

        self.running = True
        self.lastUpdate = None
        self.nextEnemySpawn = 2000

        # Set start time
        self.victoryTime += self.engine.getTicks()

        while( self.inputManager.isRunning() and self.running ):

            self.update()
            self.draw()

    def update( self ):

        # Update input
        self.inputManager.update()

        if not self.inputManager.isRunning():
            return

        # Number of ms passed
        ms = 0.0
        if self.lastUpdate:
            ms = float( self.engine.getTicks() - self.lastUpdate )
        self.lastUpdate = self.engine.getTicks()

        # Update background
        self.backgroundY += ms*1.0
        #while( self.backgroundY > self.videoManager.getScreenHeight() ):
        self.backgroundY %= self.videoManager.getScreenHeight()

        # Update player
        mouse = annchienta.Vector( self.inputManager.getMouseX(), self.inputManager.getMouseY() )
        mouse -= self.ship.pos
        mouse.normalize()
        mouse *= (ms * 0.3)
        self.ship.pos += mouse

        # Check if we should spawn enemies
        if self.engine.getTicks()<self.victoryTime:
            self.nextEnemySpawn -= ms
            while self.nextEnemySpawn <= 0 and self.inputManager.isRunning():
               
                # Spawn a new enemy
                pos = annchienta.Vector( self.mathManager.randInt( 0, videoManager.getScreenWidth() ), videoManager.getScreenHeight() + self.enemySprite.getHeight() )
                self.enemies += [ GameObject( pos, self.enemySprite ) ]
                self.nextEnemySpawn += self.mathManager.randInt( 500, 2000 )
        # Check if we should spawn the captain
        else:
            # Wait until all enemies are gone
            if not len(self.enemies) and not self.captain:

                # Spawn our captain
                pos = annchienta.Vector( videoManager.getScreenWidth()/2, videoManager.getScreenHeight()+100 )
                self.captain = GameObject( pos, annchienta.Surface("sprites/ship_captain.png") )

        # Move enemies
        for enemy in self.enemies:

            vect = None

            # Just fly on in current direction when we
            # already passed the player
            if enemy.pos.y < self.ship.pos.y:
                vect = annchienta.Vector( enemy.dir )
            # Else, approach the player's ship
            else:
                vect = self.ship.pos - enemy.pos
                vect.normalize()
                enemy.dir = annchienta.Vector( vect )

            vect.y = -1
            vect *= ( ms * 0.2 )

            enemy.pos += vect

        # Move captain
        if self.captain:
            vect = self.ship.pos - self.captain.pos
            vect.normalize()
            vect *= ( ms * 0.2 )
            self.captain.pos += vect

        # Minimum distance between player and enemies
        minDistance = 0.25*( self.enemySprite.getWidth() + self.enemySprite.getHeight() +
                             self.ship.sprite.getWidth() + self.ship.sprite.getHeight() )

        # Check for collision between enemies and
        # the player
        for enemy in self.enemies:

            if enemy.pos.distance( self.ship.pos ) < minDistance:

                # Game over
                self.running = False
                self.sceneManager.fade()
                self.sceneManager.text("We were caught by some sky pirate and executed...", None)
                self.mapManager.stop()

        # Check for collision between player and
        # the captain
        if self.captain:

            if self.captain.pos.distance( self.ship.pos ) < minDistance:

                self.running = False
                self.sceneManager.fade()
                self.sceneManager.text("We were lucky. We were caught by one of their captains, who was impressed by our flying.", None)
                self.sceneManager.text("He brouht us aboard their mothership...", None)

        # Remove enemies out of screen
        self.enemies = filter( lambda e: e.pos.y > -e.sprite.getHeight(), self.enemies )

    def draw( self ):

        self.videoManager.clear()

        # Draw background
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY) )
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY-self.videoManager.getScreenHeight()) )

        # Draw player
        self.ship.draw()

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw()
        
        # Draw captain
        if self.captain:
            self.captain.draw()

        self.videoManager.flip()

partyManager = PartyManager.getPartyManager()

# Main function, kinda
def runMiniGame():
    sceneManager = SceneManager.getSceneManager()
    videoManager = annchienta.getVideoManager()
    mapManager = annchienta.getMapManager()

    sceneManager.initDialog( [] )

    # Clear entire screen.
    videoManager.clear()
    videoManager.setColor(0,0,0)
    videoManager.drawRectangle( 0, 0, videoManager.getScreenWidth(), videoManager.getScreenHeight() )
    videoManager.flip()

    # Some intro talk.
    sceneManager.text( "August:\nAnd so we took Banver's ship in attempt to reach the Jemor continent.", None )
    sceneManager.text( "August:\nBut soon we were noticed by these sky pirates Banver mentioned.", None )
    sceneManager.text( "August:\nAt first, it seemed like there weren't too many, so we tried to evade them.", None )
    sceneManager.text( "August:\nBut then...", None )

    # Save first
    sceneManager.text( "Info: Your game was saved automatically.", None )
    path = os.path.join(os.path.expanduser("~"), ".fall-of-imiryn/save.xml")
    partyManager.save(path)

    game = Game()
    game.run()

    sceneManager.quitDialog()

    # If we made it...
    if mapManager.isRunning():
        partyManager.addRecord("fleet_caught_by_captain")
        partyManager.refreshMap()

if not partyManager.hasRecord("fleet_caught_by_captain"):
    runMiniGame()

partyManager.refreshMap()
