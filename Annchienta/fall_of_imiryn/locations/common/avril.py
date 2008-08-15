import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

avril = annchienta.getPassiveObject()
august = annchienta.getActiveObject()

sceneManager.initDialog( [avril, august] )

if not partyManager.hasRecord("inaran_intro_march"):

    sceneManager.speak( avril, "Go and talk to March." )

sceneManager.quitDialog()

