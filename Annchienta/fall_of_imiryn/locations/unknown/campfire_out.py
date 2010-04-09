import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.getCurrentMap()

august = partyManager.getPlayer()

sceneManager.initDialog( [august] )

sceneManager.speak( august, "Our campfire's ashes are still glowing.." )

sceneManager.quitDialog()

partyManager.refreshMap()

