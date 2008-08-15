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
        self.options += [ Menu.MenuItem("item", "Use an item on this party member.") ]
        self.options += [ Menu.MenuItem("confirm", "Quit this menu.") ]
        self.setOptions( self.options )

        # Set index
        self.combatantIndex = combatantIndex

        # On top.
        self.top()

    # Overwrite render: we also want to draw combatant info
    def render( self ):

        Menu.Menu.render( self )

        self.combatant = self.partyManager.team[ self.combatantIndex ]
        
        # Start by drawing the combatant itself.
        self.sceneManager.drawBox( self.sceneManager.margin, self.sceneManager.margin, self.sceneManager.margin*3+self.combatant.width, self.sceneManager.margin*3+self.combatant.height )
        self.videoManager.drawSurface( self.combatant.sprite, self.sceneManager.margin*2, self.sceneManager.margin*2, self.combatant.sx1, self.combatant.sy1, self.combatant.sx2, self.combatant.sy2 ) 


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
        
        self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )
        self.videoManager.drawString( self.sceneManager.italicsFont, "Arrow keys to cycle through party members.", 0, 0 )

        self.videoManager.popMatrix()
        
    # Overwrite update to allow left & right keys.
    def update( self ):
        
        Menu.Menu.update( self )
        if self.inputManager.keyTicked( annchienta.SDLK_LEFT ):
            self.combatantIndex -= 1

        if self.inputManager.keyTicked( annchienta.SDLK_RIGHT ):
            self.combatantIndex += 1

        self.combatantIndex %= len( self.partyManager.team )

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
                    for weapon in self.partyManager.inventory.getAvailableWeapons():
                        options += [ Menu.MenuItem( weapon, self.partyManager.inventory.getItemDescription(weapon) ) ]

                    weaponMenu.setOptions( options )
                    weaponMenu.top()
                    w = weaponMenu.pop()
                    if w is not None:
                        # Remove old weapon from combatant and add it back to inventory
                        self.partyManager.inventory.addItem( self.partyManager.team[ self.combatantIndex ].weapon.name )
                        # Set new weapon
                        self.partyManager.team[ self.combatantIndex ].setWeapon( w.name )
                        # Remove new weapon from inventory
                        self.partyManager.inventory.removeItem( w.name )

                elif ans.name == "item":
                    itemMenu = Menu.Menu( "Item", "Use an item." )
                    inv = inv = self.partyManager.inventory
                    loot = inv.getAvailableLoot()
                    items = []
                    for l in loot:
                        items += [ Menu.MenuItem( l, inv.getItemDescription(l)+" ("+str(inv.getItemCount(l))+" left)" ) ]
                    itemMenu.setOptions( items )
                    itemMenu.top()
                    item = itemMenu.pop()
                    if item is not None:
                        inv.useItemOn( item.name, self.partyManager.team[ self.combatantIndex ] )

                elif ans.name == "confirm":
                    running = False


