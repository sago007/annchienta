import annchienta
import PartyManager, SceneManager

class GameObject:

    def __init__( self, position, sprite ):

        self.videoManager = annchienta.getVideoManager()
        self.pos = position
        self.sprite = sprite

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

        # Background surface
        self.background = annchienta.Surface( "images/backgrounds/sky.png" )
        self.backgroundY = 0.0

    def run( self ):

        self.running = True
        self.lastUpdate = None

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
        self.backgroundY += ms*0.5
        while( self.backgroundY > self.videoManager.getScreenHeight() ):
            self.backgroundY -= self.videoManager.getScreenHeight()

    def draw( self ):

        self.videoManager.begin()

        # Draw background
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY) )
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY-self.videoManager.getScreenHeight()) )
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

game = Game()
game.run()

sceneManager.quitDialog()

