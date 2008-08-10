import Menu
import PartyManager
import SceneManager

partyManager = PartyManager.getPartyManager()
partyManager.heal()

sceneManager = SceneManager.getSceneManager()
sceneManager.text("Your health was restored!")

menu = Menu.Menu("Save menu.", "Save your game.")
options = [ Menu.MenuItem("save", "Save your progress."), Menu.MenuItem("cancel", "Return to the game.") ]
menu.setOptions( options )
menu.top()

ans = menu.pop()
if ans is not None:
    if ans.name == "save":
        partyManager.save( "save/save.xml" )
        sceneManager.text("Game saved!")

