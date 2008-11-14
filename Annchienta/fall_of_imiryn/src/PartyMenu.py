import annchienta
import Menu, PartyManager

# An extended menu that shows information
# about the party.
class PartyMenu( Menu.Menu ):

    def __init__( self, name="Equipment", description="Manage and view equipment.", combatantIndex = 0 ):

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
        self.sceneManager.drawBox( self.sceneManager.margin, self.sceneManager.margin, self.sceneManager.margin*3+self.combatant.width*3, self.sceneManager.margin*3+self.combatant.height )

        # Loop through combatant in team and draw their sprite. We assume the dimensions of all
        # character sprites are equal.
        for i in range(len(self.partyManager.team)):
            
            c = self.partyManager.team[ i ]

            # Draw the combatant transparantly if it's not active
            if i==self.combatantIndex:
                self.videoManager.setColor()
            else:
                self.videoManager.setColor( 255, 255, 255, 80 )

            self.videoManager.drawSurface( c.sprite, self.sceneManager.margin*2 + self.combatant.width*i, self.sceneManager.margin*2, c.sx1, c.sy1, c.sx2, c.sy2 ) 

        self.videoManager.setColor()

        x1 = self.sceneManager.margin
        y1 = self.height + self.sceneManager.margin*4
        x2 = self.videoManager.getScreenWidth() - self.sceneManager.margin
        y2 = y1 + 100

        self.videoManager.push()
        self.sceneManager.drawBox( x1, y1, x2, y2 )
        self.videoManager.translate( x1, y1 )

        self.videoManager.translate( self.sceneManager.margin, self.sceneManager.margin )
        self.videoManager.drawString( self.sceneManager.defaultFont, self.combatant.name.capitalize(), 0, 0 )

        self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )
        self.videoManager.drawString( self.sceneManager.defaultFont, "Current weapon: "+self.combatant.weapon.name.capitalize(), 0, 0 )

        self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )
        self.videoManager.drawString( self.sceneManager.defaultFont, "HP: "+str(self.combatant.healthStats["hp"])+"/"+str(self.combatant.healthStats["mhp"])+" MP: "+str(self.combatant.healthStats["mp"])+"/"+str(self.combatant.healthStats["mmp"]), 0, 0 )

        self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )
        text = reduce( lambda a,b:a+' '+b, map( lambda a: a.upper()+": "+str( self.combatant.derivedStats[a]), self.combatant.derivedStats.keys() ) )
        self.videoManager.drawString( self.sceneManager.defaultFont, str(text), 0, 0 )
        
        self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )
        self.videoManager.drawString( self.sceneManager.italicsFont, "Click combatants to select them.", 0, 0 )

        self.videoManager.pop()
        
    # Overwrite update to allow character cycling.
    def update( self ):
        
        Menu.Menu.update( self )

        # Check if one of the party members on top is clicked.
        self.combatant = self.partyManager.team[ self.combatantIndex ]
        for i in range(len(self.partyManager.team)):
            x1 = self.sceneManager.margin*2 + i*self.combatant.width
            y1 = self.sceneManager.margin*2
            x2 = x1 + self.combatant.width
            y2 = y1 + self.combatant.height
            if self.inputManager.clicked( x1, y1, x2, y2 ):
                self.combatantIndex = i
