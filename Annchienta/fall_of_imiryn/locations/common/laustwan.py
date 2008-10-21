import annchienta
import PartyManager, SceneManager

mapManager   = annchienta.getMapManager()
mathManager  = annchienta.getMathManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

laustwan = annchienta.getPassiveObject()
august = annchienta.getActiveObject()

sceneManager.initDialog( [laustwan, august] )

text = ["Kipa.", "Koo-hay.", "Poku!", "Ri-hayk?" ]
sceneManager.speak( laustwan, text[ mathManager.randInt(0, len(text)) ] )

sceneManager.quitDialog()

