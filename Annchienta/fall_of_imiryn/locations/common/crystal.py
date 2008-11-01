import annchienta
import Menu
import PartyManager
import SceneManager

cacheManager = annchienta.getCacheManager()
sound = cacheManager.getSound('sounds/crystal.ogg')

audioManager = annchienta.getAudioManager()
audioManager.playSound( sound )

partyManager = PartyManager.getPartyManager()
partyManager.heal()

sceneManager = SceneManager.getSceneManager()

sceneManager.initDialog( [annchienta.getActiveObject(), annchienta.getPassiveObject()] )
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

sceneManager.quitDialog()
