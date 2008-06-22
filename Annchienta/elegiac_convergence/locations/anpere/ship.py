import annchienta, scene, party, battle

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

thisMap = partyManager.currentMap

# Persons for scenes
player = partyManager.player
esana = annchienta.Person("esana", "locations/prison/esana.xml")
inyse = annchienta.Person("inyse", "locations/tetia/inyse.xml")
kator = annchienta.Person("kator", "locations/anpere/kator.xml")

# Set positions.
kator.setPosition( annchienta.Point( annchienta.TilePoint, 11, 6 ) )
esana.setPosition( annchienta.Point( annchienta.TilePoint, 9, 14 ) )
inyse.setPosition( annchienta.Point( annchienta.TilePoint, 11, 14 ) )
player.setPosition( annchienta.Point( annchienta.TilePoint, 13, 14 ) )

# Add persons to map
thisMap.addObject( esana )
thisMap.addObject( inyse )
thisMap.addObject( kator )

thisMap.depthSort()

# Init dialog
sceneManager.initDialog( [player, esana, inyse, kator] )

# First part of scene, ends with flashback of murder.
if not partyManager.hasRecord("anpere_met_kator"):
    
    # Kator looks away from the party.
    kator.setAnimation("standeast")

    # Move a little.
    sceneManager.move( [esana, inyse, player], [annchienta.Point(annchienta.TilePoint,9,5), annchienta.Point(annchienta.TilePoint,11,8), annchienta.Point(annchienta.TilePoint,13,5) ] )

    # Let's all look at Kator.
    player.lookAt( kator )
    esana.lookAt( kator )
    inyse.lookAt( kator )

    # Say some lines.
    sceneManager.speak( player, "Your path ends here, Kator." )
    sceneManager.speak( esana, "You murdered my father! You took his head!" )
    sceneManager.speak( inyse, "It was your fault the guards killed Cristopher!" )    

    # Kator reacts
    kator.lookAt( player )
    sceneManager.speak( kator, "The irony... are you going to stop me, Aelaan? Just liked you stopped Esana's father?" )
    sceneManager.speak( kator, "You remember now, do you not? Indeed, I was paid to kill her father, but I could never have done that without your help..." )
    
    # Aelaan backs off
    sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 13, 7 ) )
    sceneManager.speak( player, "You betrayed us..." )
    sceneManager.speak( kator, "Well, the path had to be cleared, hadn't it? Until then I found out that I couldn't take him out at all... he was pretty strong for such an old guy." )
    sceneManager.speak( player, "You... you pretended you were hurt..." )

    # Now change to flashback.
    partyManager.addRecord("anpere_met_kator")
    player.setAnimation("standsouth")
    partyManager.changeMap( "locations/anpere/flashback.xml", annchienta.Point( annchienta.TilePoint, 2, 6 ) )

sceneManager.quitDialog()

# Remove people
thisMap.removeObject( esana )
thisMap.removeObject( inyse )
thisMap.removeObject( kator )

