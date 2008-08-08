import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player
march = annchienta.Person( "march", "locations/common/march.xml" )
avril = annchienta.Person( "avril", "locations/common/avril.xml" )

augustPosition = august.getPosition().to( annchienta.IsometricPoint )
march.setPosition( augustPosition )
avril.setPosition( augustPosition )

currentMap.addObject( march )
currentMap.addObject( avril )

sceneManager.initDialog( [august, march, avril] )

sceneManager.move( [march, avril], [annchienta.Point(annchienta.IsometricPoint,augustPosition.x,augustPosition.y-30), annchienta.Point(annchienta.IsometricPoint,augustPosition.x,augustPosition.y+30)] )

march.lookAt( august )
avril.lookAt( august )

sceneManager.speak( august, "We had been walking and searching for a week.", True )
sceneManager.speak( avril, "I still can't believe they're using us for this. We're risking our lives!" )

sceneManager.speak( march, "It will be worth it. To be in the Fifth Guard is the highest rank you can get." )
sceneManager.move( march, annchienta.Point(annchienta.IsometricPoint,augustPosition.x+30,augustPosition.y-30) )

sceneManager.speak( august, "It's not worth a life." )
sceneManager.speak( avril, "I'm sorry... your brother died during one of the assignments, wasn't it?" )
sceneManager.speak( august, "This was supposed to be our last task... one final task before we would be allowed into the Fifth Guard.", True )
sceneManager.speak( august, "Fishermen from around Inaran had recently been attacked by a frightening seamonster.", True )
sceneManager.speak( august, "Our job was to exterminate it- we had now traced it down to this beach.", True )
sceneManager.speak( avril, "I'm sure it must be in that cave over there. Don't forget that you can use this magic well to heal yourself and save our progress." )

sceneManager.quitDialog()

currentMap.removeObject( march )
currentMap.removeObject( avril )

partyManager.addRecord("inaran_intro")
partyManager.refreshMap()

