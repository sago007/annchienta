import random, annchienta, Level

class Squirrel:

    yVelStart = 0.4
    yAccel = 0.0005

    def __init__( self ):
    
        # Get references
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.cacheManager = annchienta.getCacheManager()
        
        # Load sprites...
        self.sprite = self.cacheManager.getSurface("data/squirrel1.png")
        self.balloon = self.cacheManager.getSurface("data/balloon"+str(random.randint(1,3))+".png")
        
        # Set X and Y
        self.x = -self.sprite.getWidth() if random.random()<0.5 else self.videoManager.getScreenWidth()+self.sprite.getWidth()
        self.y = float(Level.treeUpperY() - self.sprite.getHeight()/2)
        
        self.xVel = 0.1 if self.x<0 else -0.1
        self.jumping = random.random()<0.6
        self.yVel = self.yVelStart
        
        # Balloontimer
        self.balloonTimer = random.randint(-3000,-1000)
        
    def draw( self ):
    
        self.videoManager.pushMatrix()
        
        # Go to main body and draw it
        self.videoManager.translate( int(self.x), int(self.y) )
        
        self.videoManager.pushMatrix()
        self.videoManager.scale( 1 if self.xVel>0 else -1, 1 )
        self.videoManager.drawSurface( self.sprite, -self.sprite.getWidth()/2, -self.sprite.getHeight()/2 )
        self.videoManager.popMatrix()
        
        # Draw the balloon
        if self.showingBalloon():
            self.videoManager.drawSurface( self.balloon, -self.balloon.getWidth()/2, -self.sprite.getHeight()/2-self.balloon.getHeight() )
        
        self.videoManager.popMatrix()
        
    def update( self, ms ):
    
        self.x += ms*self.xVel
        
        if self.jumping:
            self.y += ms*self.yVel
            if Level.yInTree( self.y+self.sprite.getHeight()/2 ) or Level.yBelowTree( self.y+self.sprite.getHeight()/2 ):
                self.y = float(Level.treeUpperY()-self.sprite.getHeight()/2)
                self.yVel = -random.uniform( 0.2, 0.4 )
            else:
                self.yVel += ms*self.yAccel

        self.balloonTimer += ms
        if self.balloonTimer > 2000:
            self.balloonTimer = random.randint(-5000,-1000)
            
    def showingBalloon( self ):
        return self.balloonTimer > 0

