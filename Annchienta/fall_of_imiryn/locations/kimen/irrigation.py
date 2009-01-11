import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.getPlayer()

sceneManager.initDialog( [august] )

if not partyManager.hasRecord("kimen_inspected_plant"):

    sceneManager.speak( august, "This looks like some sort of irrigation system." )

else:

    numberOfSystem = int( currentMap.getFileName()[-5:-4] )

    if partyManager.hasRecord( "kimen_destroyed_irrigation_"+str(numberOfSystem) ):

        sceneManager.speak( august, "We already sabotaged this irrigation system." )

    else:

        partyManager.addRecord("kimen_destroyed_irrigation_"+str(numberOfSystem))

        numberOfSystemsDestroyed = len( filter( lambda i: partyManager.hasRecord( "kimen_destroyed_irrigation_"+str(i) ), range(1,4) ) )

        if numberOfSystemsDestroyed==1:
            sceneManager.speak( august, "This seems to be some sort of irrigation system. If we cut this wire..." )
            sceneManager.text( "You sabotaged the irrigation system!" )

        elif numberOfSystemsDestroyed==2:
            sceneManager.speak( august, "That makes two of them." )

        else:
            sceneManager.speak( august, "I guess that was the last one of them. Let's head back to the ship." )

sceneManager.quitDialog()
partyManager.refreshMap()
