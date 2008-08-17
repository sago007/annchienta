import annchienta

class RaftGame:

    def __init__( self ):

        # Get references
        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.cacheManager = annchienta.getCacheManager()
        self.mapManager = annchienta.getMapManager()
        self.sceneManager = SceneManager.getSceneManager()

        # Load images
        self.background = annchienta.Surface("images/backgrounds/water.png")

        self.backgroundY = 0.0
        self.speed = 0.1

    def run( self ):

        self.running = True
        self.lastUpdate = None

        while self.running and self.inputManager.running():

            self.update()
            self.draw()

    def update( self ):

        # Update input
        self.inputManager.update()

        # Calculate number of ms passed
        ms = 0.0
        if self.lastUpdate is not None:
            ms = self.engine.getTicks() - self.lastUpdate
        self.lastUpdate = self.engine.getTicks()

        # Update background
        self.backgroundY += self.speed*ms
        while self.backgroundY >= self.background.getHeight():
            self.backgroundY -= self.background.getHeight()

    def draw( self ):

        self.videoManager.begin()

        # Draw background
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY) )
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY)-self.background.getHeight() )

        self.videoManager.end()

# Run the game
raftGame = RaftGame()
raftGame.run()

