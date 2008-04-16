import annchienta
import party

inputManager = annchienta.getInputManager()
mapManager = annchienta.getMapManager()

# If the player is not standing still, we might need
# to throw a random battle.
if not "stand" in partyManager.player.getAnimation():
    import battle
    battleManager = battle.getBattleManager()
    battleManager.throwRandomBattle()

if inputManager.keyTicked( annchienta.SDLK_RETURN ):

    import menu
    gameMenu = menu.Menu("In-Game Menu")

    o = []
    o.append( menu.MenuItem("continue", "Continue the game.") )
    o.append( menu.MenuItem("save", "Save your progress.") )
    i = menu.Menu("item", "Use an item.")
    i.setOptions( map( menu.MenuItem, ("potion", "grenade") ) )
    o.append( i )

    s = menu.Menu("spam", "Spam of menu items.")
    s.setOptions( map( lambda a:menu.MenuItem(str(a), "Bollocks.)"), range(17) ) )
    o.append( s )

    gameMenu.setOptions( o )
    gameMenu.top()
    a = gameMenu.pop()

    if a is None:
        print "Canceled."
    else:
        if a.name == "save":
            import scene
            partyManager = party.getPartyManager()
            partyManager.save("saves/save.xml")
            sceneManager = scene.getSceneManager()
            sceneManager.text("Game saved!")


