import annchienta
import Menu, PartyManager

class EquipmentMenu( Menu.Menu ):

    def __init__( self, name="Equipment", description="Manage and view equipment." ):

        # Call superclass constructor
        Menu.Menu.__init__( self, name, description )

        # Get references
        self.partyManager = PartyManager.getPartyManager()

        # Set options...
        self.options += [ Menu.MenuItem("next", "View next party member.") ]
        self.options += [ Menu.MenuItem("weapon", "Change party member weapon.") ]
        self.options += [ Menu.MenuItem("cancel", "Quit this menu.") ]
        self.setOptions( self.options )

        # On top.
        self.top()

    # Overwrite render: we also want to draw combatant info
    def render( self ):

        Menu.Menu.render( self )

        self.combatant = self.partyManager.team[ self.combatantIndex ]
        
        self.videoManager.pushMatrix()
        self.videoManager.translate( self.sceneManager.margin, self.height+self.sceneManager.margin*4 )
        self.sceneManager.drawBox( 0, 0, self.videoManager.getScreenWidth()-self.sceneManager.margin*2, 100 )

        self.videoManager.translate( self.sceneManager.margin, self.sceneManager.margin )
        self.videoManager.drawString( self.sceneManager.defaultFont, self.combatant.name.capitalize(), 0, 0 )
        self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )
        self.videoManager.drawString( self.sceneManager.defaultFont, "Current weapon: "+self.combatant.weapon.name.capitalize(), 0, 0 )

        self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )
        self.videoManager.drawString( self.sceneManager.defaultFont, "HP: "+str(self.combatant.healthStats["hp"])+"/"+str(self.combatant.healthStats["mhp"])+" MP: "+str(self.combatant.healthStats["mp"])+"/"+str(self.combatant.healthStats["mmp"]), 0, 0 )

        self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )
        text = reduce( lambda a,b:a+' '+b, map( lambda a: a.upper()+": "+str( self.combatant.derivedStats[a]), self.combatant.derivedStats.keys() ) )
        self.videoManager.drawString( self.sceneManager.defaultFont, str(text), 0, 0 )
        

        self.videoManager.popMatrix()
        
    # Pops and handles stuff.
    def run( self ):

        # Start with the first combatant
        self.combatantIndex = 0

        running = True
        while running and self.inputManager.running():

            ans = self.pop()

            if ans is None:
                running = False
            else:

                if ans.name == "next":
                    self.combatantIndex += 1
                    self.combatantIndex %= len( self.partyManager.team )

                elif ans.name == "weapon":
                    pass

                elif ans.name == "cancel":
                    running = False


