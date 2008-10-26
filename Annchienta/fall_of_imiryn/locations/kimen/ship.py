import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player

numberOfSystemsDestroyed = len( filter( lambda i: partyManager.hasRecord( "kimen_destroyed_irrigation_"+str(i) ), range(1,4) ) )

if numberOfSystemsDestroyed<3:

    sceneManager.initDialog( [august] )
    sceneManager.speak( august, "We can't leave yet." )
    sceneManager.quitDialog()

else:

    sceneManager.initDialog( [august] )
    sceneManager.speak( august, "Haha." )
    
    battleManager = BattleManager.getBattleManager()
    battleManager.runBattle( ["captain", "dragon tank", "war mage"], annchienta.Surface( "images/backgrounds/kimen.png" ) )

    sceneManager.quitDialog()

partyManager.refreshMap()
