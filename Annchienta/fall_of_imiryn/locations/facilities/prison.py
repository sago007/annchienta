import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.getCurrentMap()

august = partyManager.getPlayer()

# Addobject and stuff...
march = annchienta.Person( "march", "locations/common/march.xml" )
avril = annchienta.Person( "avril", "locations/common/avril.xml" )

march.setPosition( annchienta.Point( annchienta.TilePoint, 22, 7 ) )
avril.setPosition( annchienta.Point( annchienta.TilePoint, 24, 7 ) )
currentMap.addObject( march )
currentMap.addObject( avril )
sceneManager.initDialog( [august, march, avril] )

sceneManager.move( august, annchienta.Point( annchienta.TilePoint, 23, 7 ) )
avril.lookAt( august )

sceneManager.speak( august, "Laustwan?" )
sceneManager.speak( avril, "Laustwan indeed. I wonder why someone would lock them up? You could just order them to stay, right?" )
sceneManager.speak( march, "Is this the secret Kyzano was talking about?" )
sceneManager.speak( avril, "Doesn't seem like their is something wrong with them." )
sceneManager.speak( august, "But why would someone need that many of them?" )
sceneManager.speak( march, "And why should that person hide them, away from the Jemor continent?" )

sceneManager.fade()

partyManager.addRecord("facilities_saw_laustwan")

sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )

partyManager.refreshMap()

