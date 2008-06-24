import annchienta, scene, party, battle, combatant

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()
battleManager = battle.getBattleManager()

thisMap = partyManager.currentMap

# Fuction that adapts Kator's stats to the players
def adapt( katorEnemy ):
    stats = ["strength", "defense", "magic", "resistance", "health", "maxhealth"]
    for stat in stats:
        s = int(1.5*sum( map( lambda t: t.status.get(stat), partyManager.team ) ))
        katorEnemy.status.set(stat, s)
    

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

else:
    partyManager.addRecord("anpere_fought_kator")

    kator.setPosition( annchienta.Point( annchienta.TilePoint, 11, 6 ) )
    esana.setPosition( annchienta.Point( annchienta.TilePoint, 9, 5 ) )
    inyse.setPosition( annchienta.Point( annchienta.TilePoint, 11, 8 ) )
    player.setPosition( annchienta.Point( annchienta.TilePoint, 13, 5 ) )
    sceneManager.move( player, annchienta.Point(annchienta.TilePoint,13,6) )

    sceneManager.speak( player, "And I..." )

    sceneManager.speak( kator, "And you made the wrong choice. You should've listened to that old fool. On the other hand, it was convenient to take you out after that and cut off Barong's head." )

    sceneManager.move( player, annchienta.Point(annchienta.TilePoint,13,9) )

    sceneManager.speak( inyse, "Aelaan, wait! We can't take him without you!" )
    sceneManager.speak( player, "Why would you fight anymore... It was me after all... I'm a rotten apple..." )
    sceneManager.speak( esana, "You're not, Aelaan! We still believe in you... It was him who set you up!" )
    sceneManager.speak( inyse, "You need to help us, Aelaan!" )
    sceneManager.speak( player, "Don't you see it... I'm not fit to help anyone. Not you, not Esana. Not even myself..." )

    sceneManager.move( player, annchienta.Point(annchienta.TilePoint,13,10) )

    sceneManager.speak( esana, "Aelaan! You can't run now! You're always running! You never face the truth!" )

    player.lookAt( esana )

    sceneManager.speak( player, "But I'm so afraid to speak the truth..." )

    # Create kator enemy
    katorEnemy = battleManager.createEnemy("kator")

    # Heal party
    partyManager.heal()

    # Adapt to player stats.
    adapt( katorEnemy )
    annchienta.getLogManager().message( str(katorEnemy.status.get("strength")) )

    b = battle.Battle( partyManager.team + [katorEnemy] )
    b.background = annchienta.Surface("images/backgrounds/wooden_floor.png")
    b.run()

sceneManager.quitDialog()

# Remove people
thisMap.removeObject( esana )
thisMap.removeObject( inyse )
thisMap.removeObject( kator )
partyManager.refreshMap()

