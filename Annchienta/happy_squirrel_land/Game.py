import annchienta, Player

class Game:

    def __init__( self ):
    
        # Get nessecary references
        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.audioManager = annchienta.getAudioManager()
        self.cacheManager = annchienta.getCacheManager()
        
        # Set video mode.
        self.videoManager.setVideoMode( 480, 320, "Happy Squirrel Land!" )
        self.inputManager.setMouseVisibility( False )
        
        # Various sprites
        self.background = self.cacheManager.getSurface("data/background.png")
        self.target = self.cacheManager.getSurface("data/target.png")
        
    def run( self ):
    
        self.player = Player.Player()
    
        self.running = True
        ms = self.engine.getTicks()
        
        while self.running:
        
            self.draw()
            self.update( self.engine.getTicks()-ms )
            ms = self.engine.getTicks()
            
    def draw( self ):
    
        self.videoManager.begin()
        
        # Start with the background
        self.videoManager.drawSurface( self.background, 0, 0 )
        
        # Draw the player
        self.player.draw()
        
        # Draw the target
        self.videoManager.pushMatrix()
        self.videoManager.translate( self.inputManager.getMouseX(), self.inputManager.getMouseY() )
        self.videoManager.drawSurface( self.target, -self.target.getWidth()/2, -self.target.getHeight()/2 )
        self.videoManager.popMatrix()
        
        self.videoManager.end()
        
    def update( self, ms ):

        ms = float(ms)
        
        self.inputManager.update()
        if not self.inputManager.running():
            self.running = False
            return

        self.player.update( ms )
        

