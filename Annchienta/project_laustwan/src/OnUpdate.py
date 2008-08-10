import annchienta

engine = annchienta.getEngine()
inputManager = annchienta.getInputManager()
mapManager = annchienta.getMapManager()

# Check for random battles
if not "stand" in partyManager.player.getAnimation() and not inputManager.keyDown(annchienta.SDLK_q):
    if inputManager.getInputMode() is annchienta.InteractiveMode:
        import Battle
        Battle.throwRandomBattle()

# Quick save option to test the game. Must be disabled in the release
if inputManager.keyTicked( annchienta.SDLK_s ):
    import PartyManager
    partyManager = PartyManager.getPartyManager()
    partyManager.save( "save/save.xml" )

if inputManager.buttonTicked(1) and inputManager.getInputMode() is annchienta.InteractiveMode:

    # Create the main menu
    import Menu
    menu = Menu.Menu( "In-Game Menu", "Select action." )
    options = []

    options += [ Menu.MenuItem("continue", "Close menu and continue playing.") ]
    options += [ Menu.MenuItem("equipment", "Manage party equipment.") ]
    options += [ Menu.MenuItem("quit", "Stop playing.") ]

    menu.setOptions( options )
    menu.top()

    ans = menu.pop()

    if ans is not None:

        if ans.name == "continue":
            pass

        elif ans.name == "equipment":
            import EquipmentMenu
            equipmentMenu = EquipmentMenu.EquipmentMenu()
            equipmentMenu.run()

        elif ans.name == "quit":
            mapManager.stop()

