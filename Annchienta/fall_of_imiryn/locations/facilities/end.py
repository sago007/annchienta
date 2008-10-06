import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

# Create a whole bunch of objects/persons and set them to
# their positions.
august = partyManager.player
august.setPosition( annchienta.Point( annchienta.TilePoint, 8, 12 ) )

march = annchienta.Person( "march", "locations/common/march.xml" )
march.setPosition( annchienta.Point( annchienta.TilePoint, 9, 13 ) )
currentMap.addObject( march )

avril = annchienta.Person( "avril", "locations/common/avril.xml" )
avril.setPosition( annchienta.Point( annchienta.TilePoint, 7, 13 ) )
currentMap.addObject( avril )

ship = annchienta.StaticObject( "ship", "locations/facilities/ship.xml" )
ship.setPosition( annchienta.Point( annchienta.TilePoint, 5, 5 ) )
currentMap.addObject( ship )

# Init our dialog.
sceneManager.initDialog( [august, march, avril] )

sceneManager.speak( august, "Laustwan?" )
sceneManager.speak( avril, "Laustwan indeed. I wonder why someone would lock them up? You could just order them to stay, right?" )
sceneManager.speak( march, "Is this the secret Kyzano was talking about?" )
sceneManager.speak( avril, "Doesn't seem like their is something wrong with them." )
sceneManager.speak( august, "But why would someone need that many of them?" )
sceneManager.speak( march, "And why should that person hide them, away from the Jemor continent?" )

# Done. clean up everything.
sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )
currentMap.removeObject( ship )

