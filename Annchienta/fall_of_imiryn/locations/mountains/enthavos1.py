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
sceneManager.speak( august, "What the?" )
sceneManager.speak( enthavos, "This means the time is near for me. Follow." )
sceneManager.move( enthavos, annchienta.Point( annchienta.TilePoint, 18, 19 ) )
sceneManager.move( enthavos, annchienta.Point( annchienta.TilePoint, 17, 18 ) )
sceneManager.move( enthavos, annchienta.Point( annchienta.TilePoint, 16, 18 ) )
sceneManager.move( enthavos, annchienta.Point( annchienta.TilePoint, 16, 13 ) )
sceneManager.speak( avril, "I don't trust this at all. We better head back. I mean, a dead guy telling us to follow him..." )
sceneManager.speak( march, "Do we have any other choice? I don't want to spend the rest of my life on that stupid beach." )
sceneManager.speak( august, "This might sound strange but... he sounded pretty familiar to me." )
sceneManager.speak( avril, "What?! You knew Enthavos? Why didn't you tell me?" )
sceneManager.speak( august, "But I didn't know Enthavos... I'm pretty sure of that..." )
sceneManager.speak( march, "Maybe you did... memories are a funny thing." )
sceneManager.speak( march, "Let's follow him for now, he sounded pretty friendly." )
sceneManager.speak( avril, "Of course he sounded friendly! He's mad! Who knows what he'll do next!" )
sceneManager.speak( august, "I... I feel like we should follow him." )
sceneManager.speak( avril, "Me too, but it's just... I'm quite scared right now." )

partyManager.addRecord("mountains_first_enthavos_encounter")

sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )
currentMap.removeObject( enthavos )

partyManager.refreshMap()

