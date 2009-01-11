import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

partyManager.addRecord("inaran_cave3_scene")

# Create a whole bunch of objects/persons and set them to
# their positions.
august = partyManager.getPlayer()
augustPosition = august.getPosition().to( annchienta.TilePoint )

march = annchienta.Person( "march", "locations/common/march.xml" )
march.setPosition( annchienta.Point( annchienta.TilePoint, augustPosition.x + 1, augustPosition.y ) )
currentMap.addObject( march )

avril = annchienta.Person( "avril", "locations/common/avril.xml" )
avril.setPosition( annchienta.Point( annchienta.TilePoint, augustPosition.x, augustPosition.y+1 ) )
currentMap.addObject( avril )

# Init our dialog.
sceneManager.initDialog( [august, march, avril] )

sceneManager.speak( avril, "I still don't feel really good about leaving the Laustwan. Are you sure he will survive?" )
sceneManager.speak( march, "I am afraid he even has a better chance on surviving than we do. Who knows what this creature is..." )
sceneManager.speak( august, "You shouldn't be so pessimistic. I really think we make a good chance." )
sceneManager.speak( march, "Well, I don't. I didn't like this whole cave thing to begin with." )
sceneManager.speak( august, "Come on, March. You're the one who killed a dragon." )
sceneManager.speak( march, "I was lucky." )

sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )

partyManager.refreshMap()
