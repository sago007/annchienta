import math, annchienta, Level

class Player:

    maxRage = 20000

    def __init__( self ):
    
        # Get references
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.cacheManager = annchienta.getCacheManager()
        self.audioManager = annchienta.getAudioManager()
        
        # Load sprites...
        self.sprite = self.cacheManager.getSurface("data/player.png")
        self.gun = self.cacheManager.getSurface("data/player_gun.png")
        
        # Set X and Y
        self.x = float(self.videoManager.getScreenWidth()/2)
        self.y = float(Level.treeUpperY() - self.sprite.getHeight()/2)
        
        self.xScale = 1
        self.angle = 0
        
        self.weaponReloadTimer = -1000
        self.rage = self.maxRage
        
    def draw( self ):
    
        self.videoManager.pushMatrix()
        
        # Go to main body and draw it
        self.videoManager.translate( int(self.x), int(self.y) )
        
        self.videoManager.scale( self.xScale, 1 )
        self.videoManager.drawSurface( self.sprite, -self.sprite.getWidth()/2, -self.sprite.getHeight()/2 )
        
        # Draw the gun
        self.videoManager.rotate( self.angle if self.xScale==1 else 180-self.angle )
        self.videoManager.drawSurface( self.gun, -self.gun.getWidth()/2, -self.gun.getHeight()/2 )
        
        self.videoManager.popMatrix()
        
    def update( self, ms ):
    
        # Update rage
        if self.rage<0:
            self.rage = 0
    
        # Update x position
        if self.inputManager.keyDown( annchienta.SDLK_LEFT ):
            if self.x-self.sprite.getWidth()/2>0:
                self.x -= 0.2*ms
        if self.inputManager.keyDown( annchienta.SDLK_RIGHT ):
            if self.x+self.sprite.getWidth()/2<self.videoManager.getScreenWidth():
                self.x += 0.2*ms
            
        # Calculate angle.
        mx = float(self.inputManager.getMouseX())
        my = float(self.inputManager.getMouseY())
        dx = mx - self.x
        dx = 0.0001 if dx==0 else dx
        dy = my - self.y
        self.angle = math.degrees( math.atan( dy/dx ) )
        
        # Invert angle if we're looking to the left
        if self.x>mx:
            self.angle = 180.0 + self.angle
            self.xScale = -1
        else:
            self.xScale = 1

        # Update weapon timer
        if self.weaponReloadTimer<0:
            self.weaponReloadTimer += int(ms)
    
    def weaponLoaded( self ):
        return self.weaponReloadTimer>=0
        
    def unloadWeapon( self ):
        self.weaponReloadTimer = -1000
        self.audioManager.playSound( self.cacheManager.getSound("data/shotgun.ogg") )

