import annchienta
import Menu, PartyManager

class EquipmentMenu( Menu.Menu ):

    def __init__( self, name="Equipment", description="Manage and view equipment.", combatantIndex = 0 ):

        # Call superclass constructor
        Menu.Menu.__init__( self, name, description )

        # Get references
        self.partyManager = PartyManager.getPartyManager()

        # Set options...
        self.options += [ Menu.MenuItem("next", "View next party member.") ]
        self.options += [ Menu.MenuItem("weapon", "Change party member weapon.") ]
        self.options += [ Menu.MenuItem("cancel", "Quit this menu.") ]
        self.setOptions( self.options )

        # Set index
        self.combatantIndex = combatantIndex

        # On top.
        self.top()

    # Overwrite render: we also want to draw combatant info
    def render( self ):

        Menu.Menu.render( self )

        self.combatant = self.partyManager.team[ self.combatantIndex ]
        
        x1 = self.sceneManager.margin
        y1 = self.height + self.sceneManager.margin*4
        x2 = self.videoManager.getScreenWidth() - self.sceneManager.margin
        y2 = y1 + 100

        self.videoManager.pushMatrix()
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
        
        self.videoManager.popMatrix()
        
    # Pops and handles stuff.
    def run( self ):

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
                    weaponMenu = EquipmentMenu( "Weapon", "Select a weapon.", self.combatantIndex )
                    options = []
                    for weapon in self.partyManager.weapons:
                        if self.partyManager.hasWeaponAvailable( weapon ):
                            options += [ Menu.MenuItem( weapon, "Equip "+weapon.capitalize()+"." ) ]
                    weaponMenu.setOptions( options )
                    weaponMenu.top()
                    w = weaponMenu.pop()
                    if w is not None:
                        self.partyManager.team[ self.combatantIndex ].setWeapon( w.name )

                elif ans.name == "cancel":
                    running = False


