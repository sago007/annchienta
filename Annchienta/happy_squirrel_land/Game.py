import random, math, annchienta, Player, Squirrel, Splatter, Level

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
        self.squirrels = []
        self.splatters = []
    
        self.running = True
        ms = self.engine.getTicks()
        
        self.nextSquirrelSpawn = 1000
        
        while self.running:
        
            self.draw()
            self.update( self.engine.getTicks()-ms )
            ms = self.engine.getTicks()
            
    def draw( self ):
    
        self.videoManager.begin()
        
        # Start with the background
        self.videoManager.drawSurface( self.background, 0, 0 )
        
        # Draw the Squirrels
        map( lambda o: o.draw(), [self.player]+self.squirrels+self.splatters )
        
        # Draw the target
        self.videoManager.pushMatrix()
        self.videoManager.translate( self.inputManager.getMouseX(), self.inputManager.getMouseY() )
        self.videoManager.drawSurface( self.target, -self.target.getWidth()/2, -self.target.getHeight()/2 )
        self.videoManager.popMatrix()
        
        self.videoManager.end()
        
    def update( self, ms ):

        ms = float(ms)

        # Check if the user quit the game
        self.inputManager.update()
        if not self.inputManager.running():
            self.running = False
            return
            
        # Spawn new Squirrels
        self.nextSquirrelSpawn -= ms
        while( self.nextSquirrelSpawn < 0 ):
            self.nextSquirrelSpawn += random.randint(0,3000)
            self.squirrels += [Squirrel.Squirrel()]
        
        # Update player and squirrels and splatters
        map( lambda o: o.update(ms), [self.player]+self.squirrels+self.splatters )
        
        # Remove splatters outside of screen
        self.splatters = filter( lambda s: s.insideScreen(), self.splatters )
        
        # Remove dead squirrels outside of screen
        self.squirrels = filter( lambda s: (not s.dead) or s.insideScreen(), self.squirrels )
        
        # If the player shot...
        if self.player.weaponLoaded() and self.inputManager.buttonDown(0):
            self.shoot()
            
    def shoot( self ):

        self.player.unloadWeapon()
        
        x, y = self.player.x, self.player.y
        dx, dy = float(self.inputManager.getMouseX())-x, float(self.inputManager.getMouseY())-y
        l = math.sqrt( dx*dx + dy*dy )
        l = 1 if l==0 else l
        dx /= l
        dy /= l
        
        while Level.insideScreen(x,y):
            x += dx*5
            y += dy*5
            for s in filter( lambda s: not s.dead, self.squirrels):
                if s.hasPoint( x, y ):
                    self.nextSquirrelSpawn -= 600
                    s.dead = True
                    
                    # There will be blood
                    self.splatters += map( lambda a: Splatter.Splatter(x,y), range(20) )
                    return

