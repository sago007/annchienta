import annchienta
import MenuItem, Menu
import PartyManager
import SceneManager

cacheManager = annchienta.getCacheManager()
sound = cacheManager.getSound('sounds/crystal.ogg')
sound2 = cacheManager.getSound('sounds/save.ogg')

audioManager = annchienta.getAudioManager()
audioManager.playSound( sound )

partyManager = PartyManager.getPartyManager()
partyManager.heal()

sceneManager = SceneManager.getSceneManager()

sceneManager.initDialog( [annchienta.getActiveObject(), annchienta.getPassiveObject()] )
sceneManager.text("Your health was restored!")

menu = Menu.Menu("Save menu.", "Save your game.")
options = [ MenuItem.MenuItem("save", "Save your progress."), MenuItem.MenuItem("cancel", "Return to the game.") ]
menu.setOptions( options )
menu.top()

ans = menu.pop()
if ans is not None:
    if ans.name == "save":
        #audioManager.playSound( sound2 )
        partyManager.save( "save/save.xml" )
        sceneManager.text("The progress in your travels has been recorded.")

sceneManager.quitDialog()
