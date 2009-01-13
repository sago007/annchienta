import random, math, annchienta, Player, Squirrel, Splatter, Level

class Game:

    def __init__( self ):
    
        # Get nessecary references
        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.audioManager = annchienta.getAudioManager()
        self.cacheManager = annchienta.getCacheManager()
        
        # Various sprites
        self.background = self.cacheManager.getSurface("data/background.png")
        self.target = self.cacheManager.getSurface("data/target.png")
        
        # Main font
        self.font = annchienta.Font( "data/regular.ttf", 14 )
        
    def run( self ):
    
        self.player = Player.Player()
        self.squirrels = []
        self.splatters = []
        self.bodycount = 0
    
        self.running = True
        ms = self.engine.getTicks()
        
        self.nextSquirrelSpawn = 1000
        
        while self.running:
        
            self.draw()
            self.update( self.engine.getTicks()-ms )
            ms = self.engine.getTicks()
            
    def draw( self ):
    
        self.videoManager.clear()
        
        # Start with the background
        self.videoManager.drawSurface( self.background, 0, 0 )
        
        # Draw the Squirrels
        map( lambda o: o.draw(), [self.player]+self.squirrels+self.splatters )
        
        # Draw the target
        self.videoManager.push()
        self.videoManager.translate( self.inputManager.getMouseX(), self.inputManager.getMouseY() )
        self.videoManager.drawSurface( self.target, -self.target.getWidth()/2, -self.target.getHeight()/2 )
        self.videoManager.pop()
        
        # Draw the rage bar
        self.videoManager.setColor( 0, 0, 0, 100 )
        self.videoManager.drawRectangle( 8, 8, self.videoManager.getScreenWidth()-8, 30 )
        self.videoManager.setColor( 200, 0, 0, 255 )
        width = float(self.videoManager.getScreenWidth()-20)*float(self.player.rage)/float(self.player.maxRage)
        self.videoManager.drawRectangle( 10, 10, 10+int(width), 28 )
        self.videoManager.setColor()
        self.videoManager.drawStringCentered( self.font, "RAGE", self.videoManager.getScreenWidth()/2, 10 )
        self.videoManager.flip()
        
    def update( self, ms ):

        ms = float(ms)

        # Check if the user quit the game
        self.inputManager.update()
        if not self.inputManager.isRunning():
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
        
        # If the player shot...
        if self.player.weaponLoaded() and self.inputManager.buttonDown(0):
            self.shoot()
            
        # Subtract rage from player
        self.player.rage -= ms*len( filter( lambda s: s.showingBalloon(), self.squirrels ) )
            
        if self.player.rage <= 0:
            self.running = False
            
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
            for s in self.squirrels:
                if s.hasPoint( x, y ):
                    self.nextSquirrelSpawn -= 500
                    self.bodycount += 1
                    self.squirrels.remove(s)
                    self.audioManager.playSound( self.cacheManager.getSound("data/die.ogg") )
                    
                    # There will be blood
                    self.splatters += [Splatter.Splatter(x,y,math.radians(self.player.angle),True)]
                    self.splatters += map( lambda a: Splatter.Splatter(x,y,math.radians(self.player.angle)), range(40) )
                    return

