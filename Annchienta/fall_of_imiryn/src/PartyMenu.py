import annchienta
import MenuItem, Menu, PartyManager

# An extended menu that shows information
# about the party in the corners, but basically
# has the same functionality as a Menu.
class PartyMenu( Menu.Menu ):

    def __init__( self, name="Equipment", description="Manage and view equipment.", combatantIndex = 0 ):

        # Stuff for sounds
        self.cacheManager = annchienta.getCacheManager()
        self.audioManager = annchienta.getAudioManager()
        self.soundClickRev = self.cacheManager.getSound('sounds/click-reverse.ogg')
        self.soundClickNeg = self.cacheManager.getSound('sounds/click-negative.ogg')
        self.soundClickPos = self.cacheManager.getSound('sounds/click-positive.ogg')
        self.soundClickNeu = self.cacheManager.getSound('sounds/click-neutral.ogg')
        self.soundSave =     self.cacheManager.getSound('sounds/save.ogg')

        # Call superclass constructor
        Menu.Menu.__init__( self, name, description )

        # Get references
        self.partyManager = PartyManager.getPartyManager()

        # Set index
        self.combatantIndex = combatantIndex

    # Overwrite render: we also want to draw combatant info
    def render( self ):

        Menu.Menu.render( self )

        self.combatant = self.partyManager.team[ self.combatantIndex ]
        
        # We want to draw a box with all combatants in it.
        self.sceneManager.drawBox( self.sceneManager.getMargin(), self.sceneManager.getMargin(), self.sceneManager.getMargin()*3+self.combatant.width*3, self.sceneManager.getMargin()*3+self.combatant.height )

        # Loop through combatant in team and draw their sprite. We assume the dimensions of all
        # character sprites are equal.
        for i in range(len(self.partyManager.team)):
            
            c = self.partyManager.team[ i ]

            # Draw the combatant transparantly if it's not active
            if i==self.combatantIndex:
                self.videoManager.setColor()
            else:
                self.videoManager.setColor( 255, 255, 255, 80 )

            self.videoManager.drawSurface( c.sprite, self.sceneManager.getMargin()*2 + self.combatant.width*i, self.sceneManager.getMargin()*2, c.sx1, c.sy1, c.sx2, c.sy2 ) 

        self.videoManager.setColor()

        x1 = self.sceneManager.getMargin()
        y1 = self.height + self.sceneManager.getMargin()*4
        x2 = self.videoManager.getScreenWidth() - self.sceneManager.getMargin()
        y2 = y1 + 100

        self.videoManager.push()
        self.sceneManager.drawBox( x1, y1, x2, y2 )
        self.videoManager.translate( x1, y1 )

        self.videoManager.translate( self.sceneManager.getMargin(), self.sceneManager.getMargin() )
        self.videoManager.drawString( self.sceneManager.getDefaultFont(), self.combatant.name.capitalize(), 0, 0 )

        self.videoManager.translate( 0, self.sceneManager.getDefaultFont().getLineHeight() )
        self.videoManager.drawString( self.sceneManager.getDefaultFont(), "Current weapon: "+self.combatant.weapon.name.capitalize(), 0, 0 )

        self.videoManager.translate( 0, self.sceneManager.getDefaultFont().getLineHeight() )
        self.videoManager.drawString( self.sceneManager.getDefaultFont(), "HP: "+str(self.combatant.getHp())+"/"+str(self.combatant.getMaxHp())+" MP: "+str(self.combatant.getMp())+"/"+str(self.combatant.getMaxMp()), 0, 0 )

        self.videoManager.translate( 0, self.sceneManager.getDefaultFont().getLineHeight() )

        self.videoManager.drawString( self.sceneManager.getDefaultFont(), self.combatant.getStatsAsString(), 0, 0 )
        
        self.videoManager.translate( 0, self.sceneManager.getDefaultFont().getLineHeight() )
        self.videoManager.drawString( self.sceneManager.getItalicsFont(), "Press Tab to cycle through party members.", 0, 0 )

        self.videoManager.pop()
        
    # Overwrite update to allow character cycling.
    def update( self ):
        
        Menu.Menu.update( self )

        # Check if one of the party members on top is clicked.
        if self.inputManager.keyTicked( annchienta.SDLK_TAB ):
            self.audioManager.playSound( self.soundClickNeu ) 
            self.combatantIndex += 1

        self.combatantIndex = self.combatantIndex % len( self.partyManager.team )
        self.combatant = self.partyManager.team[ self.combatantIndex ]
