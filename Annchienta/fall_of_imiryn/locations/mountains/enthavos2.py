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

position = annchienta.Point( annchienta.TilePoint, 17, 20 )
august.setPosition( position )
march.setPosition( annchienta.Point( annchienta.TilePoint, position.x+1, position.y ) )
avril.setPosition( annchienta.Point( annchienta.TilePoint, position.x+2, position.y ) )
enthavos.setPosition( annchienta.Point( annchienta.TilePoint, position.x+1, position.y-3 ) )
currentMap.addObject( march )
currentMap.addObject( avril )
currentMap.addObject( enthavos )
sceneManager.initDialog( [august, march, avril, enthavos] )

sceneManager.move( [august, march, avril, enthavos ], [ annchienta.Point( annchienta.TilePoint, 17, 6 ), 
                                                        annchienta.Point( annchienta.TilePoint, 17, 7 ), 
                                                        annchienta.Point( annchienta.TilePoint, 17, 8 ), 
                                                        annchienta.Point( annchienta.TilePoint, 19, 7 ) ] )

august.lookAt( enthavos )
march.lookAt( enthavos )
avril.lookAt( enthavos )
enthavos.lookAt( august )

sceneManager.speak( enthavos, "We are on the Nupol continent." )
sceneManager.speak( avril, "We figured that much! Are you Enthavos? What are you doing here? And what do you want from us?!" )
sceneManager.speak( enthavos, "Mostly, I want it all to go away..." )
sceneManager.speak( enthavos, "But now the time has come for a little test. Engage!" )

partyManager.addRecord("mountains_second_enthavos_encounter")

sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )
currentMap.removeObject( enthavos )

partyManager.refreshMap()

