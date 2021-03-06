import annchienta

engine = annchienta.getEngine()
inputManager = annchienta.getInputManager()
mapManager = annchienta.getMapManager()

# Check for random battles
# Cheat: do not start them when 'q' is hold down.
if not "stand" in partyManager.getPlayer().getAnimation() and not inputManager.keyDown(annchienta.SDLK_q):
    if inputManager.getInputMode() is annchienta.InteractiveMode:
        import BattleManager
        battleManager = BattleManager.getBattleManager()
        battleManager.throwRandomBattle()

# Cheat:
# Double player's speed when pressed 'f'
if inputManager.keyTicked( annchienta.SDLK_f ):
    import PartyManager
    partyManager = PartyManager.getPartyManager()
    partyManager.getPlayer().setSpeed(2.0)

# Cheat:
# Quick save option to test the game. Must be disabled in the release
if inputManager.keyTicked( annchienta.SDLK_s ):
    import PartyManager
    partyManager = PartyManager.getPartyManager()
    partyManager.save( "save/save.xml" ) # This probably should be updated

if ( inputManager.buttonTicked(1) or inputManager.cancelKeyTicked() ) and inputManager.getInputMode() is annchienta.InteractiveMode:

    import InGameMenu
    inGameMenu = InGameMenu.InGameMenu()
    inGameMenu.run()

