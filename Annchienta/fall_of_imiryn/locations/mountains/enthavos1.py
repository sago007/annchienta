import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player

# Addobject and stuff...
march = annchienta.Person( "march", "locations/common/march.xml" )
avril = annchienta.Person( "avril", "locations/common/avril.xml" )
enthavos = annchienta.Person( "enthavos", "locations/unknown/enthavos.xml" )

position = august.getPosition().to( annchienta.TilePoint )
march.setPosition( annchienta.Point( annchienta.TilePoint, position.x+1, position.y ) )
avril.setPosition( annchienta.Point( annchienta.TilePoint, position.x+2, position.y ) )
enthavos.setPosition( annchienta.Point( annchienta.TilePoint, 19, 23 ) )
currentMap.addObject( march )
currentMap.addObject( avril )
currentMap.addObject( enthavos )
sceneManager.initDialog( [august, march, avril, enthavos] )
august.lookAt( enthavos )
march.lookAt( enthavos )
avril.lookAt( enthavos )

sceneManager.speak( enthavos, "Good. I have been waiting for you." )
sceneManager.speak( avril, "En... Enthavos?!" )
sceneManager.speak( march, "What the?" )

partyManager.addRecord("mountains_first_enthavos_encounter")

sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )
currentMap.removeObject( enthavos )

partyManager.refreshMap()

