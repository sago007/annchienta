import annchienta

inputManager = annchienta.getInputManager()
mapManager = annchienta.getMapManager()

if inputManager.keyTicked( annchienta.SDLK_RETURN ):

    import menu
    gameMenu = menu.Menu("In-Game Menu")

    o = []
    o.append( menu.MenuItem("continue", "Continue the game.") )
    o.append( menu.MenuItem("save", "Save your progress.") )
    i = menu.Menu("item", "Use an item.")
    i.setOptions( map( menu.MenuItem, ("potion", "grenade") ) )
    o.append( i )

    gameMenu.setOptions( o )
    gameMenu.top()
    a = gameMenu.pop()

    if a is None:
        print "Canceled."
    else:
        if a.name == "save":
            import party
            import scene
            partyManager = party.getPartyManager()
            partyManager.save("saves/save.xml")
            sceneManager = scene.getSceneManager()
            sceneManager.text("Game saved!")


