import scene
import annchienta
import party

mapManager = annchienta.getMapManager()
sceneManager = scene.getSceneManager()
partyManager = party.getPartyManager()

this = annchienta.getPassiveObject()
player = annchienta.getActiveObject()

sceneManager.initDialog( [player, this] )

a = sceneManager.chat( this, "Finally woke up, you stinking bag of scum?", ["Bag of scum? What the heck are you saying, man?", "Why am I here?"] )
if a is 0:
    sceneManager.chat( this, "Did you forgot you are a murderer or what?", ["A murderer?"] )
if a is 1:
    sceneManager.chat( this, "Why would you be here? Because you are a murderer, of course!", ["A murderer?"] )

sceneManager.move( this, 32, 180 )

sceneManager.quitDialog()

partyManager.addRecord("tetia_talked_to_prison_guard")
partyManager.currentMap.removeObject( this )
