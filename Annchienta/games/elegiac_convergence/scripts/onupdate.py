import annchienta
import party

engine = annchienta.getEngine()
inputManager = annchienta.getInputManager()
mapManager = annchienta.getMapManager()

# If the player is not standing still, we might need
# to throw a random battle. Also make sure that the player
# is input controlled because we do not want random
# battles during cinematic sequences.
if not "stand" in partyManager.player.getAnimation() and not inputManager.keyDown(annchienta.SDLK_q):
    if inputManager.getInputMode() is annchienta.InteractiveMode:
        import battle
        battleManager = battle.getBattleManager()
        battleManager.throwRandomBattle()

if inputManager.buttonTicked(1):

    import menu
    gameMenu = menu.Menu("In-Game Menu")

    options = [ menu.MenuItem("continue", "Continue the game."),
                menu.MenuItem("save", "Save your progress."),
                menu.MenuItem("quit", "Quit the game.") ]

    gameMenu.setOptions( options )
    gameMenu.top()
    a = gameMenu.pop()

    if a is not None:
        if a.name == "continue":
            pass
        if a.name == "save":
            import scene
            partyManager = party.getPartyManager()
            partyManager.save( engine.getWriteDirectory()+"elegiac_convergence.xml" )
            sceneManager = scene.getSceneManager()
            sceneManager.text("Game saved!")
        if a.name == "quit":
            mapManager.stop()

