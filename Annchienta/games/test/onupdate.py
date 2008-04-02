import annchienta

inputManager = annchienta.getInputManager()
mapManager = annchienta.getMapManager()

if inputManager.keyTicked( annchienta.SDLK_RETURN ):

    import menu
    gameMenu = menu.Menu("In-Game Menu")

    o = []
    o.append( menu.MenuItem("continue") )
    i = menu.Menu("item")
    i.setOptions( map( menu.MenuItem, ("potion", "grenade") ) )
    o.append( i )

    gameMenu.setOptions( o )
    a = gameMenu.pop()

    if a is None:
        print "Canceled."
    else:
        print a.name

