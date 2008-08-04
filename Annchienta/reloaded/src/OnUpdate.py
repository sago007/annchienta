import annchienta

engine = annchienta.getEngine()
inputManager = annchienta.getInputManager()
mapManager = annchienta.getMapManager()

if inputManager.buttonTicked(1):

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

