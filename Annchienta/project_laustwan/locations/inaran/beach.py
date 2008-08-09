import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player
march = currentMap.getObject( "march" )
avril = currentMap.getObject( "avril" )

sceneManager.initDialog( [august, march, avril] )

if not partyManager.hasRecord( "inaran_intro" ):

    sceneManager.speak( march, "It must be here." )
    sceneManager.speak( avril, "Are you sure?" )
    sceneManager.speak( march, "... Yes. Come over here, August." )
    sceneManager.text( "Hold down the left mouse button to move. Then click March when you're close enough." )
    partyManager.addRecord( "inaran_intro" )



sceneManager.quitDialog()

partyManager.refreshMap()

