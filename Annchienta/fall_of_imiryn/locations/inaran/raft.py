import annchienta

class RaftObject:

    def __init__( self, surface, position ):

        self.videoManager = annchienta.getVideoManager()

        self.surface = surface
        self.position = position

    def draw( self ):

        self.videoManager.pushMatrix()
        self.videoManager.translate( int(self.position.x), int(self.position.y) )
        self.videoManager.drawSurface( self.surface, -self.surface.getWidth()/2, -self.surface.getHeight()/2 )
        self.videoManager.popMatrix()

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

        # Initial positions
        self.backgroundY = 0.0
        self.speed = 0.1

        self.raft = RaftObject( annchienta.Surface("sprites/raft.png"), annchienta.Vector( self.videoManager.getScreenWidth()/2, self.videoManager.getScreenHeight()/2 ) )

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

        # Move raft towards cursor
        mouse = annchienta.Vector( self.inputManager.getMouseX(), self.inputManager.getMouseY() )
        mouse -= self.raft.position
        mouse.normalize()
        self.raft.position += mouse*self.speed*ms

    def draw( self ):

        self.videoManager.begin()

        # To make the cave tremble
        self.videoManager.translate( annchienta.randInt(-1,1), annchienta.randInt(-1,1) )

        # Draw background
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY) )
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY)-self.background.getHeight() )

        # draw player
        self.raft.draw()

        self.videoManager.end()

# Run the game
raftGame = RaftGame()
raftGame.run()

