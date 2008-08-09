import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

laustwan = annchienta.getPassiveObject()
august = annchienta.getActiveObject()

sceneManager.initDialog( [laustwan, august] )

text = ["Kipa.", "Koo-hay.", "Poku!", "Ri-hayk?" ]
sceneManager.speak( laustwan, text[ annchienta.randInt(0, len(text)-1) ] )

sceneManager.quitDialog()

