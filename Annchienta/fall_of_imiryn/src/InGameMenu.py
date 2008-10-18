import annchienta
import Menu, PartyMenu
import PartyManager

class InGameMenu:

    # Main Constructor
    def __init__( self ):

        # General references
        self.mapManager   = annchienta.getMapManager()
        self.inputManager = annchienta.getInputManager()
        self.partyManager = PartyManager.getPartyManager()

        self.menu = Menu.Menu( "In-Game Menu", "Select action." )

        options = []

        # An option that does nothing.
        options += [ Menu.MenuItem("continue", "Close menu and continue playing.") ]

        # A submenu for party management.
        options += [ Menu.MenuItem( "party management", "Change equipment, heal...") ]

        # An option to quit.
        options += [ Menu.MenuItem("quit", "Stop playing.") ]

        self.menu.setOptions( options )
        self.menu.top()

    # Runs this in game menu
    def run( self ):

        ans = self.menu.pop()

        if ans is not None:

            if ans.name == "continue":
                pass

            elif ans.name == "party management":
                self.partyManagement()

            elif ans.name == "quit":
                self.mapManager.stop()

    # Pops an equipment menu
    def partyManagement( self ):

        partyManagementMenu = PartyMenu.PartyMenu( "party management", "Manage your party." )

        # Set options...
        partyOptions = []
        partyOptions += [ Menu.MenuItem("weapon", "Change party member weapon.") ]
        partyOptions += [ Menu.MenuItem("item", "Use an item on this party member.") ]
        partyOptions += [ Menu.MenuItem("confirm", "Quit this menu.") ]
        partyManagementMenu.setOptions( partyOptions )

        # Top right corner
        partyManagementMenu.topRight()

        popping = True
        while popping and self.inputManager.running():

            ans = partyManagementMenu.pop()

            # The user canceled
            if ans is None:
                popping = False
                
            else:

                if ans.name == "weapon":

                    # Construct a weapon menu
                    weaponMenu = PartyMenu.PartyMenu( "Weapon", "Select a weapon.", partyManagementMenu.combatantIndex )
                        
                    # Create options
                    weaponOptions = []
                    for weaponName in self.partyManager.inventory.getAvailableWeapons():

                        weapon = self.partyManager.inventory.getWeapon( weaponName )

                        # Create a tooltip with the stats
                        toolTip = self.partyManager.inventory.getItemDescription(weaponName) + '\n'
                        toolTip += reduce( lambda a,b: a+' '+b, map( lambda k: k.upper()+': '+str(weapon.stats[k]), weapon.stats.keys() ) )

                        weaponOptions += [ Menu.MenuItem( weaponName, toolTip ) ]

                    # Add a confirm option
                    weaponOptions += [ Menu.MenuItem( "confirm", "Go back to the party management menu." ) ]

                    weaponMenu.setOptions( weaponOptions )
                    weaponMenu.topRight()

                    weaponPopping = True

                    while weaponPopping and self.inputManager.running():

                        w = weaponMenu.pop()
                        if w is not None:
                            if w.name != "confirm":
                                # Remove old weapon from combatant and add it back to inventory
                                self.partyManager.inventory.addItem( self.partyManager.team[ weaponMenu.combatantIndex ].weapon.name )
                                # Set new weapon
                                self.partyManager.team[ weaponMenu.combatantIndex ].setWeapon( w.name )
                                # Remove new weapon from inventory
                                self.partyManager.inventory.removeItem( w.name )
                            else:
                                weaponPopping = False
                        else:
                            weaponPopping = False

                    # Update combatant
                    partyManagementMenu.combatantIndex = weaponMenu.combatantIndex

                elif ans.name == "item":

                    # Create an item menu to choose from.
                    itemMenu = PartyMenu.PartyMenu( "Item", "Use an item.", partyManagementMenu.combatantIndex )
                    inv = self.partyManager.inventory

                    # Add all items
                    loot = inv.getAvailableLoot()
                    items = []
                    for l in loot:
                        items += [ Menu.MenuItem( l, inv.getItemDescription(l)+" ("+str(inv.getItemCount(l))+" left)" ) ]

                    # Add a confirm option
                    items += [ Menu.MenuItem( "confirm", "Go back to the party management menu." ) ]

                    # Set options
                    itemMenu.setOptions( items )
                    itemMenu.topRight()

                    itemPopping = True
                    while itemPopping and self.inputManager.running():

                        # Choose item
                        item = itemMenu.pop()
                        if item is not None:
                            if item.name != "confirm":
                                inv.useItemOn( item.name, self.partyManager.team[ itemMenu.combatantIndex ] )
                            else:
                                itemPopping = False
                        else:
                            itemPopping = False

                    # Update combatant
                    partyManagementMenu.combatantIndex = itemMenu.combatantIndex

                elif ans.name == "confirm":
                    popping = False

