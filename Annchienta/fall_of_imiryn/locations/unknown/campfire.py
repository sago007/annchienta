import annchienta
import PartyManager, SceneManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.getCurrentMap()

august = partyManager.getPlayer()

if partyManager.hasRecord("unknown_can_leave"):
    pass

elif not (partyManager.hasRecord("unknown_found_flints") and partyManager.hasRecord("unknown_found_wood") and partyManager.hasRecord("unknown_found_food")): # If not all_objects_collected

    sceneManager.initDialog( [august] )

    sceneManager.speak( august, "This looks like the perfect place to start a fire... and we really need some food." )

    if not partyManager.hasRecord("unknown_found_flints"):
        sceneManager.speak( august, "We need something to start a fire... something like a flint." )
    if not partyManager.hasRecord("unknown_found_wood"):
        sceneManager.speak( august, "Some dry wood or something similar is nessecary here." )
    if not partyManager.hasRecord("unknown_found_food"):
        sceneManager.speak( august, "I wonder if we could find something edible." )
        if partyManager.hasRecord("unknown_found_wood"):
            sceneManager.speak( august, "Perhaps if I can find a good fishing spot..." )

    sceneManager.quitDialog()

else:

    # Addobject and stuff...
    march = annchienta.Person( "march", "locations/common/march.xml" )
    avril = annchienta.Person( "avril", "locations/common/avril.xml" )
    enthavos = annchienta.Person( "enthavos", "locations/unknown/enthavos.xml" )
    august.setPosition( annchienta.Point( annchienta.TilePoint, 18, 17 ) )
    currentMap.addObject( march, annchienta.Point( annchienta.TilePoint, 17, 15 ) )
    currentMap.addObject( avril, annchienta.Point( annchienta.TilePoint, 19, 15 ) )
    currentMap.addObject( enthavos, annchienta.Point( annchienta.TilePoint, 0, 0 ) )
    sceneManager.initDialog( [august, march, avril, enthavos] )
    sceneManager.fade()

    partyManager.addRecord( "unknown_night" )

    sceneManager.speak( august, "So... let me light this fire..." )

    # Start fire
    campfire = currentMap.getObject( "campfire" )
    campfire.setAnimation( "burn" )

    sceneManager.speak( march, "I think I know where we are." )
    sceneManager.speak( avril, "And that is?" )
    sceneManager.speak( march, "The Nupol continent. I'm quite sure. I've been here once with my old man." )
    sceneManager.speak( march, "The very south of the Nupol continent, of course..." )
    sceneManager.speak( august, "March's father is quite a rich man. He has high function at the Ministry of Laustwan, and is required to travel a lot.", True )
    sceneManager.speak( august, "... The Ministry of Laustwan makes sure nobody abuses these creatures, as the Laustwan would offer their help to anyone.", True )
    sceneManager.speak( august, "This lead me to think March's father would be a kind and gentle man.", True )
    sceneManager.speak( august, "Well, maybe he is, but March doesn't seem to like his father, though.", True )
    sceneManager.speak( march, "The air feels differently here... less polluted..." )
    sceneManager.speak( august, "The Nupol continent is situared to the south of the Jemor continent, where we came from.", True )
    sceneManager.speak( august, "Our Imiryn Empire only recently conquered this continent... and we only have some trade cities in the north of this continent.", True )
    sceneManager.speak( august, "We absolutely have to reach the trade cities in the north. From there, we can get back to the Jemor continent." )
    sceneManager.speak( avril, "But I heard the inland was a very, very dangerous area?" )
    sceneManager.speak( august, "Hmm. Someone has obviously been here before us... and I mean, we're in the Fifth Guard now." )
    sceneManager.speak( avril, "The Fifth Guard... somehow that doesn't mean very much to me right now. I wonder why I wanted to join it so badly in the first place..." )
    sceneManager.speak( avril, "This whole test, all the tasks we completed seem so useless now." )
    sceneManager.speak( march, "Don't say that... we saved many lives defeating that sea creature." )
    sceneManager.speak( avril, "But is that worth our own lives?" )
    sceneManager.speak( august, "Avril... we won't die. I won't die in the Fifth Guard. My brother did, but I won't." )
    sceneManager.speak( march, "Your brother died in the Fifth Guard as well?" )
    sceneManager.speak( august, "He fought Enthavos." )
    sceneManager.speak( march, "Enthavos... once a legend in the Fifth Guard." )
    sceneManager.speak( august, "Enthavos was one of the best fighters in the Fifth Guard. He was a legend.", True )
    sceneManager.speak( august, "One day, however, he went mad... he tried to kill the Empire.", True )
    sceneManager.speak( august, "They needed fifty soldiers from the Fifth Guard to defeat him. My brother died in this battle.", True )
    sceneManager.speak( avril, "They say Enthavos still wanders the world. My grandmother saw him one day." )
    sceneManager.speak( march, "Avril... grow up. Those are fairy tales." )
    sceneManager.speak( avril, "No, I am serious." )
    sceneManager.speak( march, "Whatever. I'm going to get some sleep. We'd better all do that. Tomorrow, we head inland." )
    sceneManager.speak( avril, "But we're not alone here! I mean, the axe we found, the... We take guards." )
    sceneManager.speak( march, "Alright, allright. You take the first guard, then." )
    sceneManager.speak( august, "I'll take the second guard." )
    sceneManager.speak( march, "Then I'll take the last guard. See you all tomorrow." )

    # Enthavos walks near
    enthavos.setPosition( annchienta.Point( annchienta.TilePoint, 10, 22 ) )
    sceneManager.move( enthavos, annchienta.Point( annchienta.TilePoint, 17, 22 ), True )
    sceneManager.speak( avril, "Guys, I have the feeling someone is watching us." )
    sceneManager.speak( march, "I don't hear nor see anything..." )
    sceneManager.move( enthavos, annchienta.Point( annchienta.TilePoint, 10, 27 ), True )

    sceneManager.fade()
    partyManager.removeRecord( "unknown_night" )
    partyManager.addRecord( "unknown_can_leave" )

    sceneManager.quitDialog()
    currentMap.removeObject( march )
    currentMap.removeObject( avril )
    currentMap.removeObject( enthavos )

partyManager.refreshMap()

