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
        self.mapManager   = annchienta.getMapManager()
        self.mathManager  = annchienta.getMathManager()
        self.sceneManager = SceneManager.getSceneManager()

        # Load images
        self.background = annchienta.Surface("images/backgrounds/water.png")
        self.cacheManager.getSurface("sprites/rock1.png")
        self.cacheManager.getSurface("sprites/rock2.png")

        # Initial positions
        self.backgroundY = 0.0
        self.speed = 0.1
        self.nextSpawn = 500
        self.rocks = []

        self.raft = RaftObject( annchienta.Surface("sprites/raft.png"), annchienta.Vector( self.videoManager.getScreenWidth()/2, self.videoManager.getScreenHeight()/2 ) )

    def run( self ):

        self.running = True
        self.lastUpdate = None

        # Two minutes
        self.start = self.engine.getTicks()
        self.end = self.engine.getTicks()+60000
        
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

        # Update rocks
        for rock in self.rocks:
            rock.position.y += self.speed*ms

        # New spawns
        self.nextSpawn -= ms
        while self.nextSpawn < 0 and self.engine.getTicks()<self.end:
            surface = self.cacheManager.getSurface( "sprites/rock" + str( self.mathManager.randInt( 1, 3 ) ) + ".png" )
            position = annchienta.Vector( self.mathManager.randInt( 0, self.videoManager.getScreenWidth() ) , -surface.getHeight() )
            rock = RaftObject( surface, position )
            self.rocks.insert( 0, rock )
            self.nextSpawn += self.mathManager.randInt( 300, 1000 )
        
        # Remove rocks out of vision
        self.rocks = filter( lambda r: r.position.y < self.videoManager.getScreenHeight()+r.surface.getHeight(), self.rocks )

        # Now check for collision with rocks
        for rock in self.rocks:

            dist = 0.2*float( self.raft.surface.getWidth()+self.raft.surface.getHeight()+rock.surface.getWidth()+rock.surface.getHeight() )
            if rock.position.distance( self.raft.position ) < dist:
                self.running = False
                self.mapManager.stop()
                self.sceneManager.gameOver()

        # Stop if we're out the cave
        if self.engine.getTicks()>=self.end and not len(self.rocks):
            self.running = False

    def draw( self ):

        self.videoManager.begin()

        # To make the cave tremble
        tremble = 3
        self.videoManager.translate( self.mathManager.randInt(-tremble,tremble+1), self.mathManager.randInt(-tremble,tremble+1) )

        # Draw background
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY) )
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY)-self.background.getHeight() )

        # Draw rocks
        for rock in self.rocks:
            rock.draw()

        # draw player
        self.raft.draw()

        self.videoManager.end()

# Run the game
raftGame = RaftGame()
raftGame.run()

