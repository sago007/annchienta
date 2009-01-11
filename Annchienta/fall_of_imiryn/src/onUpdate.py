import annchienta

engine = annchienta.getEngine()
inputManager = annchienta.getInputManager()
mapManager = annchienta.getMapManager()

# Check for random battles
if not "stand" in partyManager.getPlayer().getAnimation() and not inputManager.keyDown(annchienta.SDLK_q):
    if inputManager.getInputMode() is annchienta.InteractiveMode:
        import BattleManager
        battleManager = BattleManager.getBattleManager()
        battleManager.throwRandomBattle()

# Quick save option to test the game. Must be disabled in the release
if inputManager.keyTicked( annchienta.SDLK_s ):
    import PartyManager
    partyManager = PartyManager.getPartyManager()
    partyManager.save( "save/save.xml" )

if inputManager.buttonTicked(1) and inputManager.getInputMode() is annchienta.InteractiveMode:

    import InGameMenu
    inGameMenu = InGameMenu.InGameMenu()
    inGameMenu.run()

