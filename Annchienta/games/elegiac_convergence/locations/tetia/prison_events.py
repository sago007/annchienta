import annchienta
import scene
import party

sceneManager = scene.getSceneManager()
partyManager = party.getPartyManager()

player = partyManager.player

# The first event
if not partyManager.hasRecord("tetia_prison_awakening"):
    partyManager.addRecord("tetia_prison_awakening")
    player.setPosition( annchienta.Point( annchienta.TilePoint, 8, 5 ) )
    sceneManager.initDialog( [player] )
    sceneManager.thoughts( "Ouch..." )
    sceneManager.thoughts( "My head is all fuzzy-like..." )
    sceneManager.speak( player, "Where the heck am I?" )
    sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 8, 2 ) )
    sceneManager.speak( player, "This can't be prison?" )
    sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 9, 2 ) )
    sceneManager.speak( player, "Why can't I remember anything?" )
    sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 7, 2 ) )
    sceneManager.speak( player, "What the heck is going on?" )
    sceneManager.quitDialog()
    partyManager.refreshMap()
