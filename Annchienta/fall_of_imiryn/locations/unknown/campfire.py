import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.currentMap

august = partyManager.player

if not (partyManager.hasRecord("unknown_found_flints") and partyManager.hasRecord("unknown_found_wood") and partyManager.hasRecord("unknown_found_food")): # If not all_objects_collected

    sceneManager.initDialog( [august] )

    sceneManager.speak( august, "This looks like the perfect place to start a fire... and we really need some food." )

    if not partyManager.hasRecord("unknown_found_flints"):
        sceneManager.speak( august, "We need something to start a fire... something like a flint." )
    if not partyManager.hasRecord("unknown_found_wood"):
        sceneManager.speak( august, "Some dry wood or something similar is nessecary here." )
    if not partyManager.hasRecord("unknown_found_food"):
        sceneManager.speak( august, "I wonder if we could find something edible." )

    sceneManager.quitDialog()

else:

    # Addobject and stuff...
    march = annchienta.Person( "march", "locations/common/march.xml" )
    avril = annchienta.Person( "avril", "locations/common/avril.xml" )
    august.setPosition( annchienta.Point( annchienta.TilePoint, 18, 17 ) )
    march.setPosition( annchienta.Point( annchienta.TilePoint, 17, 15 ) )
    avril.setPosition( annchienta.Point( annchienta.TilePoint, 19, 15 ) )
    currentMap.addObject( march )
    currentMap.addObject( avril )
    sceneManager.initDialog( [august, march, avril] )
    sceneManager.fade()

    partyManager.addRecord( "unknown_night" )

    sceneManager.speak( august, "So... let me light this fire..." )

    # Start fire
    campfire = currentMap.getObject( "campfire" )
    campfire.setAnimation( "burn" )

    sceneManager.speak( march, "I think I know where we are." )
    sceneManager.speak( avril, "And that is?" )
    sceneManager.speak( march, "The Nupol continent. I'm quite sure. I've been here once with my old man." )
    sceneManager.speak( august, "March's father is quite a rich man. He has high function at the Ministry of Laustwan, and is required to travel a lot.", True )
    sceneManager.speak( august, "March doesn't seem to like his father, though for some strange reason.", True )
    sceneManager.speak( march, "The air feels differently here... less polluted..." )
    sceneManager.speak( august, "The Nupol continent is situared to the south of the Jemor continent, where we came from.", True )
    sceneManager.speak( august, "Our Imiryn Empire only recently conquered this continent... and we only have some trade cities in the north of this continent.", True )
    sceneManager.speak( march, "The very south of the Nupol continent, of course..." )
    sceneManager.speak( avril, "But I heard that was a very, very dangerous area?" )
    sceneManager.speak( august, "Hmm. Someone has obviously been here before us... but I mean, we're in the Fifth Guard now." )
    sceneManager.speak( avril, "The Fifth Guard... somehow that doesn't mean very much to me right now. I wonder why I wanted to join it so badly in the first place..." )
    sceneManager.speak( avril, "I think I wanted to join because... I don't know, but my whole life, I had this feeling that something... strange is going on in this world." )
    sceneManager.speak( august, "What do you mean?" )
    sceneManager.speak( avril, "I'm not sure what it is... but I know someone, or some force... needs my help. So I thought if I'd join the Fifth Guard, I'd..." )
    sceneManager.speak( avril, "You know what? Never mind... It's probably nothing anyway. And now we're stuck in the middle of nowhere, all because of this stupid mission." )
    sceneManager.speak( march, "Don't say that... we saved lives defeating that sea creature." )
    sceneManager.speak( avril, "But is that worth our own lives?" )
    sceneManager.speak( august, "Avril... we won't die. I won't die in the Fifth Guard. My brother did, but I won't." )
    sceneManager.speak( march, "Your brother died in the Fifth Guard?" )
    sceneManager.speak( august, "He fought Enthavos." )
    sceneManager.speak( march, "Enthavos... once a legend in the Fifth Guard." )
    sceneManager.speak( august, "Enthavos was one of the best fighters in the Fifth Guard. He was a legend.", True )
    sceneManager.speak( august, "One day, however, he went mad... he tried to kill the Empire.", True )
    sceneManager.speak( august, "They needed fifty soldiers from the Fifth Guard to defeat him. My brother died in this battle.", True )
    sceneManager.speak( avril, "They say he still wanders the world. My grandmother saw him one day!" )
    sceneManager.speak( march, "Avril... grow up. Those are fairy tales." )
    sceneManager.speak( march, "I'm going to get some sleep. We'd better all do that. Tomorrow, we head inland." )

    sceneManager.fade()
    partyManager.removeRecord( "unknown_night" )

    sceneManager.quitDialog()
    currentMap.removeObject( march )
    currentMap.removeObject( avril )

partyManager.refreshMap()

