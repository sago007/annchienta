import annchienta
import PartyManager, SceneManager, BattleManager

mapManager = annchienta.getMapManager()
videoManager = annchienta.getVideoManager()
partyManager = PartyManager.getPartyManager()
sceneManager = SceneManager.getSceneManager()

currentMap = partyManager.getCurrentMap()

partyManager.addRecord("fleet_met_pirates")

# Create a whole bunch of objects/persons and set them to
# their positions.
august = partyManager.getPlayer()
august.setPosition( annchienta.Point( annchienta.TilePoint, 4, 4 ) )

march = annchienta.Person( "march", "locations/common/march.xml" )
currentMap.addObject( march, annchienta.Point( annchienta.TilePoint, 4, 5 ) )

avril = annchienta.Person( "avril", "locations/common/avril.xml" )
currentMap.addObject( avril, annchienta.Point( annchienta.TilePoint, 4, 6 ) )

pirate1 = annchienta.Person( "emenver", "locations/fleet/pirate1.xml" )
currentMap.addObject( pirate1, annchienta.Point( annchienta.TilePoint, 7, 5 ) )

pirate2 = annchienta.Person( "hoche", "locations/fleet/pirate2.xml" )
currentMap.addObject( pirate2, annchienta.Point( annchienta.TilePoint, 7, 6 ) )

# Init our dialog.
sceneManager.initDialog( [august, march, avril, pirate1, pirate2] )

# Set correct headings and animations.
august.lookAt( pirate1 )
march.lookAt( pirate1 )
avril.lookAt( pirate1 )
pirate1.lookAt( august )
pirate2.lookAt( august )

sceneManager.speak( pirate1, "Well, well. Members of the Fifth Guard, in an Empirial Aircraft." )
sceneManager.speak( pirate1, "Yet, you seem different than the other soldiers who attacked us." )
sceneManager.move( pirate1, annchienta.Point( annchienta.TilePoint, 7, 3 ), True )
sceneManager.speak( pirate1, "You fly pretty well, too. You evaded most of fighters." )
sceneManager.move( pirate1, annchienta.Point( annchienta.TilePoint, 5, 3 ), True )
sceneManager.speak( pirate1, "It's almost a shame I'll have to kill you." )
pirate1.lookAt( avril )

sceneManager.speak( august, "You dirty..." )
sceneManager.speak( avril, "Wait!" )
sceneManager.move( avril, annchienta.Point( annchienta.TilePoint, 5, 6 ), True )
sceneManager.speak( avril, "We are allied to the Imiryn Empire no more." )

sceneManager.move( pirate2, annchienta.Point( annchienta.TilePoint, 8, 6 ), True )
sceneManager.speak( pirate2, "Yeah right. Anyone can say that. We need proof." )

sceneManager.speak( pirate1, "What side are you on, if you're not with the Empire?" )
sceneManager.speak( march, "We have no side anymore. We are driven by our heart, not by orders." )
sceneManager.speak( pirate1, "You almost sound like a pirate." )

sceneManager.speak( march, "Then release us! We're not headed to the Imperial City, but to a place north of it." )
sceneManager.speak( march, "We promise we won't stand in your way." )

sceneManager.speak( pirate2, "We will release you. Aren't we friendly pirates? We only demand one little thing." )
sceneManager.speak( pirate1, "We want the flight access code of your aircraft to the outer Imiryn Imperial City regions." )

sceneManager.speak( march, "We can't do that... That would be betrayal." )
sceneManager.speak( pirate2, "Didn't you just say you weren't allied to Imiryn anymore?" )
sceneManager.speak( march, "Yeah, but..." )
sceneManager.speak( pirate1, "Would you rather die?" )
sceneManager.speak( august, "I would've gladly died. But no more. I just saw an Imperial general kill my brother." )
sceneManager.speak( august, "Besides... Kyzano said what we're fighting for is more important than our Empire." )
sceneManager.speak( avril, "I agree." )

sceneManager.speak( august, "I couldn't believe it had come this far. Betraying our own Empire.", True )
sceneManager.speak( august, "I kept telling myself I did this for the greater good, to complete Kyzano's mission.", True )
sceneManager.speak( august, "After all, he had died for this.", True )
sceneManager.speak( august, "I kept telling myself I did this for the greater good. Not to save our own dirty little lives...", True )

sceneManager.speak( pirate1, "Fly with us until we reach the Jemor continent. We'll release you, and even give you back your ship." )

sceneManager.fade()
sceneManager.text( "And so we arrived in Kimen, where we would find the truth, as Kyzano had told us.", None )
sceneManager.text( "It looked just like a regular plantation, until we had a better look at the plants...", None )

# Done. clean up everything.
sceneManager.quitDialog()
currentMap.removeObject( march )
currentMap.removeObject( avril )
currentMap.removeObject( pirate1 )
currentMap.removeObject( pirate2 )

# Go to Kimen.
partyManager.changeMap( "locations/kimen/plantation1.xml", annchienta.Point( annchienta.TilePoint, 24, 15 ) )

