import annchienta, Level

class Player:

    def __init__( self ):
    
        # Get references
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.cacheManager = annchienta.getCacheManager()
        
        # Load sprites...
        self.sprite = self.cacheManager.getSurface("data/squirrel1.png")
        
        # Set X and Y
        self.x = float(self.videoManager.getScreenWidth()/2)
        self.y = float(Level.treeUpperY() - self.sprite.getHeight()/2)
        
        self.xScale = 1
        
    def draw( self ):
    
        self.videoManager.pushMatrix()
        self.videoManager.translate( int(self.x), int(self.y) )
        self.videoManager.scale( self.xScale, 1 )
        self.videoManager.drawSurface( self.sprite, -self.sprite.getWidth()/2, -self.sprite.getHeight()/2 )
        self.videoManager.popMatrix()
        
    def update( self, ms ):
    
        if self.inputManager.keyDown( annchienta.SDLK_LEFT ):
            self.xScale = -1
            self.x -= 0.2*ms
        if self.inputManager.keyDown( annchienta.SDLK_RIGHT ):
            self.xScale = 1
            self.x += 0.2*ms
            
