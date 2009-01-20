import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.getCurrentMap()

august = partyManager.getPlayer()
ship   = annchienta.getPassiveObject()

numberOfSystemsDestroyed = len( filter( lambda i: partyManager.hasRecord( "kimen_destroyed_irrigation_"+str(i) ), range(1,4) ) )

if numberOfSystemsDestroyed<3:

    sceneManager.initDialog( [august] )
    sceneManager.speak( august, "We can't leave yet." )
    sceneManager.quitDialog()

else:

    # Calculate new positions and add actors.
    shipPosition = ship.getPosition().to( annchienta.TilePoint )

    august.setPosition( annchienta.Point( annchienta.TilePoint, shipPosition.x+1, shipPosition.y+1 ) )

    march = annchienta.Person( "march", "locations/common/march.xml" )
    currentMap.addObject( march, annchienta.Point( annchienta.TilePoint, shipPosition.x+2, shipPosition.y+1 ) )

    avril = annchienta.Person( "avril", "locations/common/avril.xml" )
    currentMap.addObject( avril, annchienta.Point( annchienta.TilePoint, shipPosition.x+1, shipPosition.y+2 ) )

    captain = annchienta.Person( "captain", "locations/kimen/captain.xml" )
    currentMap.addObject( captain, annchienta.Point( annchienta.TilePoint, shipPosition.x+1, shipPosition.y+7 ) )
    
    sceneManager.initDialog( [august, march, avril, captain] )

    sceneManager.fade()

    sceneManager.speak( captain, "This is as far as you go." )

    august.lookAt( captain )
    march.lookAt( captain )
    avril.lookAt( captain )

    sceneManager.move( captain, annchienta.Point( annchienta.TilePoint, shipPosition.x+1, shipPosition.y+3 ) )

    sceneManager.speak( captain, "Bring the dragon tank!" )

    battleManager = BattleManager.getBattleManager()
    won = battleManager.runBattle( ["captain", "dragon tank", "war mage"], annchienta.Surface( "images/backgrounds/kimen.png" ), False )

    currentMap.removeObject( captain )

    if won:
        sceneManager.speak( avril, "We did it..." )
        sceneManager.speak( august, "I revenged my brother." )
        sceneManager.speak( march, "We freed the Laustwan." )
        sceneManager.speak( august, "We can now return to Imiryn. The upper class will hate us, but..." )
        sceneManager.speak( august, "That won't matter. We did what we have to do... When we tell the truth, we will be accepted." )
        sceneManager.fade()
        execfile("locations/kimen/epilogue.py")

    sceneManager.quitDialog()
    currentMap.removeObject( march )
    currentMap.removeObject( avril )

