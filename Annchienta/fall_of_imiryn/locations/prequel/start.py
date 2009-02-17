import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.getCurrentMap()

august = partyManager.getPlayer()

sceneManager.initDialog( [august] )

sceneManager.text( "Click and hold down the left mouse button somewhere on the screen to walk in that direction." )
sceneManager.text( "Click with the left mouse button on interesting objects and people to interact with them." )
sceneManager.text( "Alternatively, use the arrow keys to walk around, and press the spacebar to interact with objects." )

sceneManager.quitDialog()

partyManager.addRecord('prequel_start')
partyManager.refreshMap()
