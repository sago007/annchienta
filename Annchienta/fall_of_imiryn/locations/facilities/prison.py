import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player

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
sceneManager.speak( march, "The principle of peaceful actions." )
sceneManager.speak( avril, "The what?" )
sceneManager.speak( march, "I think someone is using these Laustwan as tools of war..." )
sceneManager.speak( august, "What?" )
sceneManager.speak( march, "What else could it be? Why else would someone want that many Laustwan, and hide away from the Jemor continent?" )
sceneManager.speak( august, "So that was what my brother was talking about... a terrible secret indeed." )
sceneManager.speak( avril, "We need to set them free. We have to!" )

sceneManager.fade()

partyManager.addRecord("facilities_saw_laustwan")

sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )

partyManager.refreshMap()

