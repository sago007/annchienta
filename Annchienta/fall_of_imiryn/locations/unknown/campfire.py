import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player

if not (partyManager.hasRecord("unknown_found_flint") and partyManager.hasRecord("unknown_found_wood") and partyManager.hasRecord("unknown_found_food")): # If not all_objects_collected

    sceneManager.initDialog( [august] )

    sceneManager.speak( august, "This looks like the perfect place to start a fire... and we really need some food." )

    if not partyManager.hasRecord("unknown_found_flint"):
        sceneManager.speak( august, "We need something to start a fire... something like a flint." )
    if not partyManager.hasRecord("unknown_found_wood"):
        sceneManager.speak( august, "Some dry wood or something similar is nessecary here." )
    if not partyManager.hasRecord("unknown_found_food"):
        sceneManager.speak( august, "I wonder if we could find something edible." )

else:

    # Addobject and stuff...
    march = currentMap.getObject( "march" )
    avril = currentMap.getObject( "avril" )
    sceneManager.initDialog( [august, march, avril] )

sceneManager.quitDialog()

partyManager.refreshMap()

