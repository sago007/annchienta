import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

march = annchienta.getPassiveObject()
august = annchienta.getActiveObject()

sceneManager.initDialog( [march, august] )

if not partyManager.hasRecord("inaran_intro_march"):

    sceneManager.speak( march, "Can you see that cave over there? That must be it." )

    sceneManager.speak( august, "I guess... finally..." )

    sceneManager.speak( august, "We had been searching these Inaran areas for a week.", True )
    sceneManager.speak( august, "It was supposed to be our last test before we could join the Fifth Guard.", True )

    partyManager.addRecord("inaran_intro_march")

sceneManager.quitDialog()

