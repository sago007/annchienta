import annchienta
import PartyManager, SceneManager

class GameObject:

    def __init__( self, position, sprite ):

        self.videoManager = annchienta.getVideoManager()
        self.pos = position
        self.sprite = sprite
        self.dir = annchienta.Vector( 0, 0 )

    def draw( self ):

        self.videoManager.pushMatrix()
        self.videoManager.translate( self.pos.x, self.pos.y )
        self.videoManager.drawSurface( self.sprite, -self.sprite.getWidth()/2, -self.sprite.getHeight()/2 )
        self.videoManager.popMatrix()

class Game:

    def __init__( self ):

        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.cacheManager = annchienta.getCacheManager()

        # Background spriteace
        self.background = annchienta.Surface( "images/backgrounds/sky.png" )
        self.backgroundY = 0.0

        # Create a ship for the player
        self.ship = GameObject( annchienta.Vector( videoManager.getScreenWidth()/2, videoManager.getScreenHeight()/2 ),
                                annchienta.Surface( "sprites/ship_small.png" ) )

        # Load sprites into cache
        self.cacheManager.getSurface("sprites/ship_pirate.png")

        # All enemies
        self.enemies = []

    def run( self ):

        self.running = True
        self.lastUpdate = None
        self.nextEnemySpawn = 0

        while( self.inputManager.running() and self.running ):

            self.update()
            self.draw()

    def update( self ):

        # Update input
        self.inputManager.update()

        # Number of ms passed
        ms = 0.0
        if self.lastUpdate:
            ms = float( self.engine.getTicks() - self.lastUpdate )
        self.lastUpdate = self.engine.getTicks()

        # Update background
        self.backgroundY += ms*1.0
        while( self.backgroundY > self.videoManager.getScreenHeight() ):
            self.backgroundY -= self.videoManager.getScreenHeight()

        # Update player
        mouse = annchienta.Vector( self.inputManager.getMouseX(), self.inputManager.getMouseY() )
        mouse -= self.ship.pos
        mouse.normalize()
        mouse *= (ms * 0.3)
        self.ship.pos += mouse

        # Check if we should spawn enemies
        self.nextEnemySpawn -= ms
        while self.nextEnemySpawn <= 0:
            
            # Spawn a new enemy
            sprite = self.cacheManager.getSurface("sprites/ship_pirate.png")
            pos = annchienta.Vector( annchienta.randInt( 0, videoManager.getScreenWidth() ), videoManager.getScreenHeight() + sprite.getHeight() )
            self.enemies += [ GameObject( pos, sprite ) ]
            self.nextEnemySpawn += annchienta.randInt( 500, 2000 )

        # Move enemies
        for enemy in self.enemies:

            vect = None

            if enemy.pos.y < self.ship.pos.y:
                vect = annchienta.Vector( enemy.dir )
            else:
                vect = self.ship.pos - enemy.pos
                vect.normalize()
                enemy.dir = annchienta.Vector( vect )

            vect.y = -1

            vect *= ( ms * 0.2 )

            enemy.pos += vect

        # Remove enemies out of screen
        self.enemies = filter( lambda e: e.pos.y > -e.sprite.getHeight(), self.enemies )

    def draw( self ):

        self.videoManager.begin()

        # Draw background
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY) )
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY-self.videoManager.getScreenHeight()) )

        # Draw player
        self.ship.draw()

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw()

        self.videoManager.end()


# Main function, kinda
sceneManager = SceneManager.getSceneManager()
partyManager = PartyManager.getPartyManager()
videoManager = annchienta.getVideoManager()

sceneManager.initDialog( [] )

# Clear entire screen.
videoManager.begin()
videoManager.setColor(0,0,0)
videoManager.drawRectangle( 0, 0, videoManager.getScreenWidth(), videoManager.getScreenHeight() )
videoManager.end()

# Some intro talk.
sceneManager.text( "August:\nAnd so we took Banver's ship in attempt to reach the Jemor continent.", None )
sceneManager.text( "August:\nBut soon we were noticed by these sky pirates Banver mentioned.", None )
sceneManager.text( "August:\nAt first, it seemed like there weren't too many, so we tried to evade them.", None )
sceneManager.text( "August:\nBut then...", None )

# Save first
sceneManager.text( "Info: Your game was saved automatically.", None )
partyManager.save( "save/save.xml" )

game = Game()
game.run()

sceneManager.quitDialog()

