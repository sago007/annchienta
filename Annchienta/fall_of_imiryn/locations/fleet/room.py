import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

partyManager.addRecord("fleet_met_pirate2s")

# Create a whole bunch of objects/persons and set them to
# their positions.
august = partyManager.player
august.setPosition( annchienta.Point( annchienta.TilePoint, 4, 4 ) )

march = annchienta.Person( "march", "locations/common/march.xml" )
march.setPosition( annchienta.Point( annchienta.TilePoint, 4, 5 ) )
currentMap.addObject( march )

avril = annchienta.Person( "avril", "locations/common/avril.xml" )
avril.setPosition( annchienta.Point( annchienta.TilePoint, 4, 6 ) )
currentMap.addObject( avril )

pirate1 = annchienta.Person( "pirate1", "locations/fleet/pirate1.xml" )
pirate1.setPosition( annchienta.Point( annchienta.TilePoint, 7, 5 ) )
currentMap.addObject( pirate1 )

pirate2 = annchienta.Person( "pirate2", "locations/fleet/pirate2.xml" )
pirate2.setPosition( annchienta.Point( annchienta.TilePoint, 7, 6 ) )
currentMap.addObject( pirate2 )

# Init our dialog.
sceneManager.initDialog( [august, march, avril, pirate1, pirate2] )

# Set correct headings and animations.
august.lookAt( pirate1 )
march.lookAt( pirate1 )
avril.lookAt( pirate1 )
pirate1.lookAt( august )
pirate2.lookAt( august )

sceneManager.speak( avril, "Yeah, but I treat him right! I don't lock him up." )

# Done. clean up everything.
sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )
currentMap.removeObject( pirate1 )
currentMap.removeObject( pirate2 )
