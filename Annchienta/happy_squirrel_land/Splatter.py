import random, math, annchienta, Level

class Splatter:

    def __init__( self, x, y, angle, squirrel=False ):
    
        self.squirrel = squirrel
    
        # Get references
        self.videoManager = annchienta.getVideoManager()
        self.cacheManager = annchienta.getCacheManager()
        
        # Load sprites...
        if self.squirrel:
            self.sprite = self.cacheManager.getSurface("data/squirrel1.png")
        else:
            self.sprite = self.cacheManager.getSurface("data/splatter"+str(random.randint(1,5))+
".png")
        # Set X and Y
        self.x = x
        self.y = y

        self.velStart = random.uniform( 0.15, 0.25 )
        self.yAccel = random.uniform( 0.0002, 0.0008 )
        
        # Choose start direction
        angle += random.uniform(-math.pi/8, math.pi/8)
        self.xVel = self.velStart*math.cos( angle )
        self.yVel = self.velStart*math.sin( angle )
        
        self.sticksToTree = random.random()<0.5
        
        self.xScale = -1 if random.random()<0.5 else 1
        self.yScale = -1 if self.squirrel else 1
        
    def draw( self ):
    
        self.videoManager.push()
        
        # Go to main body and draw it
        self.videoManager.translate( int(self.x), int(self.y) )

        self.videoManager.scale( self.xScale, self.yScale )
            
        self.videoManager.drawSurface( self.sprite, -self.sprite.getWidth()/2, -self.sprite.getHeight()/2 )
        
        self.videoManager.pop()
        
    def update( self, ms ):
    
        # Update coordinates
        self.x += ms*self.xVel
        self.y += ms*self.yVel
        
        if Level.yAboveTree( self.y ):
            self.yVel += ms*self.yAccel
        elif Level.yInTree( self.y ):
            self.yVel = 0.002 if self.sticksToTree else 0.02
            self.xVel = 0
        else:
            self.yVel = 0.5
            self.xVel = 0
            
    def insideScreen( self ):
    
        return self.y-self.sprite.getHeight()/2<=self.videoManager.getScreenHeight()

