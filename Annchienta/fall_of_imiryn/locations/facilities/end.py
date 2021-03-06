import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.getCurrentMap()

partyManager.addRecord("facilities_met_banver")

# Create a whole bunch of objects/persons and set them to
# their positions.
august = partyManager.getPlayer()
august.setPosition( annchienta.Point( annchienta.TilePoint, 8, 12 ) )

march = annchienta.Person( "march", "locations/common/march.xml" )
currentMap.addObject( march, annchienta.Point( annchienta.TilePoint, 9, 12 ) )

avril = annchienta.Person( "avril", "locations/common/avril.xml" )
currentMap.addObject( avril, annchienta.Point( annchienta.TilePoint, 7, 12 ) )

ship = annchienta.StaticObject( "ship", "locations/facilities/ship.xml" )
currentMap.addObject( ship, annchienta.Point( annchienta.TilePoint, 5, 6 ) )

kyzano = annchienta.Person( "kyzano", "locations/unknown/enthavos.xml" )
currentMap.addObject( kyzano, annchienta.Point( annchienta.TilePoint, 7, 7 ) )

banver = annchienta.Person( "banver", "locations/facilities/banver.xml" )
currentMap.addObject( banver, annchienta.Point( annchienta.TilePoint, 7, 8 ) )

soldier1 = annchienta.Person( "soldier", "locations/facilities/soldier.xml" )
currentMap.addObject( soldier1, annchienta.Point( annchienta.TilePoint, 6, 9 ) )

soldier2 = annchienta.Person( "soldier", "locations/facilities/soldier.xml" )
currentMap.addObject( soldier2, annchienta.Point( annchienta.TilePoint, 8, 9 ) )

# Init our dialog.
sceneManager.initDialog( [august, march, avril, kyzano, banver, soldier1, soldier2] )

# Set correct headings and animations.
august.lookAt( banver )
march.lookAt( banver )
avril.lookAt( banver )
kyzano.setAnimation("dying")
banver.lookAt( kyzano )
soldier1.lookAt( kyzano )
soldier2.lookAt( kyzano )

sceneManager.speak( banver, "I admire the fact you made it this far, Kyzano." )
sceneManager.speak( banver, "If I hadn't been here, you might even have succeeded." )
sceneManager.speak( banver, "But now, the time has come for you to die." )
sceneManager.speak( banver, "And this time for real. The Empire has no mercy for traitors like you!" )

sceneManager.speak( august, "Hold it right there!" )

banver.lookAt( august )
soldier1.lookAt( august )
soldier2.lookAt( august )

sceneManager.speak( banver, "To see you again under these circumstances. We all thought you failed the test after we found the cave collapsed." )
sceneManager.speak( banver, "This is good news, however. You are welcome to join the Fifth Guard. Of course you won't tell anyone what happened here." )
sceneManager.speak( avril, "Yeah right, you fucking monster! You cannot treat Laustwan like that. If this is the way of the Fifth Guard, then it you can stick it right up your..." )
sceneManager.speak( march, "Avril, language." )
sceneManager.speak( banver, "If you were regular civilians, I would've executed you right away. It's only because you are such capable warriors that you have a choice: to join, or to die." )
sceneManager.speak( august, "I just saw you trying to kill my brother. What do you fucking think we'll do?" )
sceneManager.speak( avril, "We cannot allow anyone to mistreat Laustwan like that. They're not tools!" )
sceneManager.speak( banver, "Ignorant fools. You have no idea what is going on here, do you?" )
sceneManager.speak( march, "Then tell us, if you are so confident." )
sceneManager.speak( banver, "Hmm. I guess you have the right to know the truth before your death." )
sceneManager.speak( banver, "I bet you have a Laustwan at home, too?" )
sceneManager.speak( avril, "Yeah, but I treat him right! I don't lock him up." )
sceneManager.speak( banver, "Idiots. Did you never wonder what Laustwan are?" )
sceneManager.speak( soldier1, "General... We are receiving new reports. A massive fleet of sky pirates is gathering near our capital." )
sceneManager.speak( soldier2, "Why can't those arrogant thieves leave us alone?" )
sceneManager.speak( banver, "Alright then. Let's finish these fools off and fly back." )

battleManager = BattleManager.getBattleManager()
won = battleManager.runBattle( ["soldier", "banver", "soldier"], annchienta.Surface("images/backgrounds/facilities.png"), False )
#won = True

# Soldiers come, soldiers go...
currentMap.removeObject( banver )
currentMap.removeObject( soldier1 )
currentMap.removeObject( soldier2 )

if won:

    sceneManager.move( [august, march, avril], [ annchienta.Point( annchienta.TilePoint, 8, 8 ), 
                                                 annchienta.Point( annchienta.TilePoint, 9, 9 ), 
                                                 annchienta.Point( annchienta.TilePoint, 7, 9 ) ] )
    sceneManager.speak( august, "Brother! Are you alright?" )
    sceneManager.speak( kyzano, "Have been better..." )
    sceneManager.speak( august, "It's over now. We stopped him." )
    sceneManager.speak( kyzano, "I know... that's good... but it's not all over yet. You have his airship now..." )
    sceneManager.speak( kyzano, "Fly to Kimen, a place north of the Imiryn Imperial City." )
    sceneManager.speak( august, "To do what? How long do we have to keep on fighting? We don't even know what we're fighting for! I want answers... please." )
    sceneManager.speak( kyzano, "Near Kimen, you will find a plantation... there, you will find the truth..." )
    sceneManager.speak( kyzano, "I don't know everything myself, but..." )
    sceneManager.speak( kyzano, "But trust me, it's worth more than our empire..." )
    sceneManager.speak( kyzano, "Remember me when it is all over... goodbye..." )
    sceneManager.speak( august, "..." )

    sceneManager.fade()

# Done. clean up everything.
sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )
currentMap.removeObject( ship )
currentMap.removeObject( kyzano )

if won:
    partyManager.changeMap( "locations/fleet/room.xml", annchienta.Point( annchienta.TilePoint, 4, 4 ) )
else:
    partyManager.refreshMap()
