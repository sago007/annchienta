import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

# Get the player and plant
august = partyManager.getPlayer()
plant = annchienta.getPassiveObject()
sceneManager.initDialog( [august, plant] )

if partyManager.hasRecord("kimen_inspected_plant"):

    sceneManager.speak( august, "It is strange that these plants cause all this evil..." )
    sceneManager.quitDialog()

else:

    partyManager.addRecord("kimen_inspected_plant")

    sceneManager.speak( august, "What are these plants? Let's have a closer look..." )

    sceneManager.quitDialog()

    # Calculate new positions and add actors.
    plantPosition = plant.getPosition().to( annchienta.TilePoint )

    august.setPosition( annchienta.Point( annchienta.TilePoint, plantPosition.x+1, plantPosition.y+1 ) )

    march = annchienta.Person( "march", "locations/common/march.xml" )
    march.setPosition( annchienta.Point( annchienta.TilePoint, plantPosition.x+2, plantPosition.y+1 ) )
    currentMap.addObject( march )

    avril = annchienta.Person( "avril", "locations/common/avril.xml" )
    avril.setPosition( annchienta.Point( annchienta.TilePoint, plantPosition.x+1, plantPosition.y+2 ) )
    currentMap.addObject( avril )

    captain = annchienta.Person( "captain", "locations/kimen/captain.xml" )
    captain.setPosition( annchienta.Point( annchienta.TilePoint, plantPosition.x+1, plantPosition.y+7 ) )
    currentMap.addObject( captain )
    
    sceneManager.initDialog( [august, march, avril, captain] )

    august.lookAt( plant )
    march.lookAt( plant )
    avril.lookAt( plant )

    sceneManager.fade()
    sceneManager.speak( march, "What could link these plants to the Laustwan locked up in those facilities?" )

    sceneManager.speak( captain, "There is no such thing as Laustwan. There are only humans..." )

    august.lookAt( captain )
    march.lookAt( captain )
    avril.lookAt( captain )

    sceneManager.speak( avril, "What the fuck are you talking about?" )
    sceneManager.speak( march, "Avril, language." )

    sceneManager.move( captain, annchienta.Point( annchienta.TilePoint, plantPosition.x+1, plantPosition.y+3 ) )

    sceneManager.speak( captain, "Like I said, Laustwan are humans... It is only because of these plants here that we are able to enslave them." )
    sceneManager.speak( captain, "The perfect drug... the perfect slaves... for the perfect Empire." )

    sceneManager.speak( august, "But that's inhuman!" )
    sceneManager.speak( captain, "The inhabitants of the Empire are happy to live comfortable lives thanks to the Laustwan." )
    sceneManager.speak( captain, "They do not ask questions, because they need the Laustwand. Which idiot would bite the hand that feeds?" )

    sceneManager.speak( captain, "Well, isn't it ironic? You were so close to freeing the Laustwan." )
    sceneManager.speak( captain, "After all, these plants here are the only good ones left. We lost a lot of them in our war against the pirates." )
    sceneManager.speak( captain, "And that's why we will guard these plantation, no matter what! Now die!" )

    battleManager = BattleManager.getBattleManager()
    won = battleManager.runBattle( ["captain", "war mage", "captain"], annchienta.Surface( "images/backgrounds/kimen.png" ), False )
    
    
    currentMap.removeObject( captain )
    sceneManager.quitDialog()
    
    if won:
        sceneManager.initDialog( [august, avril, march ] )
        
        sceneManager.speak( avril, "Did you hear that? We have to destroy this plantation, quick!" )
        sceneManager.speak( august, "Then Empire will not be able to make the drugs for some time..." )
        sceneManager.speak( march, "And then the people will find out the truth!" )
        
        sceneManager.quitDialog()
        
    currentMap.removeObject( march )
    currentMap.removeObject( avril )

partyManager.refreshMap()
