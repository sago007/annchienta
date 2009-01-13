import annchienta
import MenuItem, Menu, PartyMenu
import PartyManager

class InGameMenu(object):

    # Main Constructor
    def __init__( self ):

        # General references
        self.mapManager   = annchienta.getMapManager()
        self.inputManager = annchienta.getInputManager()
        self.partyManager = PartyManager.getPartyManager()

        self.menu = Menu.Menu( "In-Game Menu", "Select action." )

        options = []

        # An option that does nothing.
        options += [ MenuItem.MenuItem("continue", "Close menu and continue playing.") ]

        # A submenu for party management.
        options += [ MenuItem.MenuItem( "party", "Change equipment, heal...") ]

        # An option to quit.
        options += [ MenuItem.MenuItem("quit", "Stop playing.") ]

        self.menu.setOptions( options )
        self.menu.top()

    # Runs this in game menu
    def run( self ):

        menuItem = self.menu.pop()

        if menuItem is not None:

            if menuItem.getName() == "continue":
                pass

            elif menuItem.getName() == "party":
                self.partyManagement()

            elif menuItem.getName() == "quit":
                self.mapManager.stop()

    # Generate the weapon menu.
    def createWeaponMenu( self, combatantIndex ):

        weaponMenu = PartyMenu.PartyMenu( "Weapon", "Select a weapon.", combatantIndex )
            
        # Create options
        weaponOptions = []
        for weaponName in self.partyManager.getInventory().getAvailableWeapons():

            weapon = self.partyManager.getInventory().getWeapon( weaponName )

            # Create a tooltip with the stats
            toolTip = self.partyManager.getInventory().getItemDescription(weaponName) + '\n'
            toolTip += weapon.getStatsAsString() 

            weaponOptions += [ MenuItem.MenuItem( weaponName, toolTip ) ]

        # Add a confirm option
        weaponOptions += [ MenuItem.MenuItem( "confirm", "Go back to the party management menu." ) ]

        weaponMenu.setOptions( weaponOptions )
        weaponMenu.topRight()

        return weaponMenu

    # Generate the item menu.
    def createItemMenu( self, combatantIndex ):

        # Construct the menu
        itemMenu = PartyMenu.PartyMenu( "Item", "Use an item.", combatantIndex )
        inv = self.partyManager.getInventory()

        # Add all items
        loot = inv.getAvailableLoot()
        items = []
        for l in loot:
            items += [ MenuItem.MenuItem( l, inv.getItemDescription(l)+" ("+str(inv.getItemCount(l))+" left)" ) ]

        # Add a confirm option
        items += [ MenuItem.MenuItem( "confirm", "Go back to the party management menu." ) ]

        # Set options
        itemMenu.setOptions( items )
        itemMenu.topRight()

        return itemMenu


    # Pops an equipment menu
    def partyManagement( self ):

        partyManagementMenu = PartyMenu.PartyMenu( "party management", "Manage your party." )

        # Set options...
        partyOptions = []
        partyOptions += [ MenuItem.MenuItem("weapon", "Change party member weapon.") ]
        partyOptions += [ MenuItem.MenuItem("item", "Use an item on this party member.") ]
        partyOptions += [ MenuItem.MenuItem("confirm", "Quit this menu.") ]
        partyManagementMenu.setOptions( partyOptions )

        # Top right corner
        partyManagementMenu.topRight()

        popping = True
        while popping and self.inputManager.isRunning():

            menuItem = partyManagementMenu.pop()

            # The user canceled
            if menuItem is None:
                popping = False
                
            else:

                if menuItem.getName() == "weapon":

                    # Construct a weapon menu
                    weaponMenu = self.createWeaponMenu( partyManagementMenu.combatantIndex )
                    weaponPopping = True

                    while weaponPopping and self.inputManager.isRunning():

                        w = weaponMenu.pop()
                        if w is not None:
                            if w.name != "confirm":
                                # Remove old weapon from combatant and add it back to inventory
                                self.partyManager.getInventory().addItem( self.partyManager.team[ weaponMenu.combatantIndex ].weapon.name )
                                # Set new weapon
                                self.partyManager.team[ weaponMenu.combatantIndex ].setWeapon( w.name )
                                # Remove new weapon from inventory
                                self.partyManager.getInventory().removeItem( w.name )
                                # Create a new weaponmenu
                                weaponMenu = self.createWeaponMenu( weaponMenu.combatantIndex )
                            else:
                                weaponPopping = False
                        else:
                            weaponPopping = False

                    # Update combatant
                    partyManagementMenu.combatantIndex = weaponMenu.combatantIndex

                elif menuItem.getName() == "item":

                    # Create an item menu to choose from.
                    itemMenu = self.createItemMenu( partyManagementMenu.combatantIndex )

                    # Get a shortcut to the inventory
                    inv = self.partyManager.getInventory()

                    itemPopping = True

                    while itemPopping and self.inputManager.isRunning():

                        # Choose item
                        item = itemMenu.pop()
                        if item is not None:
                            if item.name != "confirm":
                                inv.useItemOn( item.name, self.partyManager.team[ itemMenu.combatantIndex ] )
                                itemMenu = self.createItemMenu( itemMenu.combatantIndex )
                            else:
                                itemPopping = False
                        else:
                            itemPopping = False

                    # Update combatant
                    partyManagementMenu.combatantIndex = itemMenu.combatantIndex

                elif menuItem.getName() == "confirm":
                    popping = False

