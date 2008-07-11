import random, math, annchienta, Level

class Splatter:

    velStart = 0.1
    yAccel = 0.0005

    def __init__( self, x, y ):
    
        # Get references
        self.videoManager = annchienta.getVideoManager()
        self.cacheManager = annchienta.getCacheManager()
        
        # Load sprites...
        self.sprite = self.cacheManager.getSurface("data/splatter"+str(random.randint(1,5))+
".png")
        # Set X and Y
        self.x = x
        self.y = y
        
        # Choose start direction
        angle = random.uniform(0, 2*math.pi)
        self.xVel = self.velStart*math.cos( angle )
        self.yVel = self.velStart*math.sin( angle )
        
        self.sticksToTree = random.random()<0.5
        
    def draw( self ):
    
        self.videoManager.pushMatrix()
        
        # Go to main body and draw it
        self.videoManager.translate( int(self.x), int(self.y) )

        self.videoManager.drawSurface( self.sprite, -self.sprite.getWidth()/2, -self.sprite.getHeight()/2 )
        
        self.videoManager.popMatrix()
        
    def update( self, ms ):
    
        # Update coordinates
        self.x += ms*self.xVel
        self.y += ms*self.yVel
        
        if Level.yAboveTree( self.y ):
            self.yVel += ms*self.yAccel
        elif Level.yInTree( self.y ):
            self.yVel = 0 if self.sticksToTree else 0.02
            self.xVel = 0
        else:
            self.yVel = 0.5
            self.xVel = 0
            
    def insideScreen( self ):
    
        return self.y-self.sprite.getHeight()/2<=self.videoManager.getScreenHeight()

