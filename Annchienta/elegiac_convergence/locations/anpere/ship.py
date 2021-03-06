import annchienta, scene, party, battle, combatant

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()
battleManager = battle.getBattleManager()
videoManager = annchienta.getVideoManager()
audioManager = annchienta.getAudioManager()
mapManager = annchienta.getMapManager()

thisMap = partyManager.currentMap

# Fuction that adapts Kator's stats to the players
def adapt( jelobatEnemy ):
    stats = ["strength", "defense", "magic", "resistance", "health", "maxhealth"]
    for stat in stats:
        s = int(1.5*sum( map( lambda t: t.status.get(stat), partyManager.team ) ))
        jelobatEnemy.status.set(stat, s)
    

# Persons for scenes
player = partyManager.player
esana = annchienta.Person("esana", "locations/prison/esana.xml")
inyse = annchienta.Person("inyse", "locations/tetia/inyse.xml")
jelobat = annchienta.Person("jelobat", "locations/anpere/jelobat.xml")

# Set positions.
jelobat.setPosition( annchienta.Point( annchienta.TilePoint, 11, 6 ) )
esana.setPosition( annchienta.Point( annchienta.TilePoint, 9, 14 ) )
inyse.setPosition( annchienta.Point( annchienta.TilePoint, 11, 14 ) )
player.setPosition( annchienta.Point( annchienta.TilePoint, 13, 14 ) )

# Add persons to map
thisMap.addObject( esana )
thisMap.addObject( inyse )
thisMap.addObject( jelobat )

thisMap.depthSort()

# Init dialog
sceneManager.initDialog( [player, esana, inyse, jelobat] )

# First part of scene, ends with flashback of murder.
if not partyManager.hasRecord("anpere_met_jelobat"):
    
    # Kator looks away from the party.
    jelobat.setAnimation("standeast")

    # Move a little.
    sceneManager.move( [esana, inyse, player], [annchienta.Point(annchienta.TilePoint,9,5), annchienta.Point(annchienta.TilePoint,11,8), annchienta.Point(annchienta.TilePoint,13,5) ] )

    # Let's all look at Kator.
    player.lookAt( jelobat )
    esana.lookAt( jelobat )
    inyse.lookAt( jelobat )

    # Say some lines.
    sceneManager.speak( player, "Your path ends here, Kator." )
    sceneManager.speak( esana, "You murdered my father! You took his head!" )
    sceneManager.speak( inyse, "It was your fault the guards killed Cristopher!" )    

    # Kator reacts
    jelobat.lookAt( player )
    sceneManager.speak( jelobat, "The irony... are you going to stop me, Aelaan? Just liked you stopped Esana's father?" )
    sceneManager.speak( jelobat, "You remember now, do you not? Indeed, I was paid to kill her father, but I could never have done that without your help..." )
    
    # Aelaan backs off
    sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 13, 7 ) )
    sceneManager.speak( player, "You betrayed us..." )
    sceneManager.speak( jelobat, "Well, the path had to be cleared, hadn't it? Until then I found out that I couldn't take him out at all... he was pretty strong for such an old guy." )
    sceneManager.speak( player, "You... you pretended you were hurt..." )

    # Now change to flashback.
    partyManager.addRecord("anpere_met_jelobat")
    player.setAnimation("standsouth")
    partyManager.changeMap( "locations/anpere/flashback.xml", annchienta.Point( annchienta.TilePoint, 2, 6 ) )

else:
    partyManager.addRecord("anpere_fought_jelobat")

    jelobat.setPosition( annchienta.Point( annchienta.TilePoint, 8, 6 ) )
    jelobat.setAnimation( "standsouth" )
    esana.setPosition( annchienta.Point( annchienta.TilePoint, 9, 10 ) )
    inyse.setPosition( annchienta.Point( annchienta.TilePoint, 11, 8 ) )
    player.setPosition( annchienta.Point( annchienta.TilePoint, 13, 5 ) )
    sceneManager.move( player, annchienta.Point(annchienta.TilePoint,13,7) )

    sceneManager.speak( player, "And I..." )

    sceneManager.speak( jelobat, "And you made the wrong choice. You should've listened to that old fool. On the other hand, it was convenient to take you out after that and cut off Barong's head." )

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

    # Create jelobat enemy
    jelobatEnemy = battleManager.createEnemy("jelobat")

    # Heal party
    partyManager.heal()

    # Adapt to player stats.
    adapt( jelobatEnemy )
    annchienta.getLogManager().message( str(jelobatEnemy.status.get("strength")) )

    b = battle.Battle( partyManager.team + [jelobatEnemy] )
    b.background = annchienta.Surface("images/backgrounds/wooden_floor.png")
    
    audioManager.playMusic("music/anpere.ogg")
    b.run()
    #b.won = True

    if b.won:

        audioManager.playMusic("music/title.ogg")
        # Fall from boat
        sceneManager.speak( jelobat, "Why... you..." )
        sceneManager.move( jelobat, annchienta.Point( annchienta.TilePoint, 7, 6 ) )
        jelobat.setAnimation( "standsouth" )
        sceneManager.speak( jelobat, "Argh..." )
        sceneManager.move( jelobat, annchienta.Point( annchienta.TilePoint, 6, 6 ) )

        sceneManager.speak( inyse, "We did it." )

        sceneManager.speak( player, "I'm... I'm so sorry for everything... but I have to speak the truth... I love you." )
        sceneManager.speak( esana, "So much has been happening..." )
        sceneManager.speak( esana, "I never... I... I just don't know it anymore..." )
        sceneManager.speak( esana, "Hold me." )

        sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 9, 10 ) )

        sceneManager.fadeOut(0,0,0,1000)
        videoManager.setClearColor(0,0,0)
        videoManager.clear()
        videoManager.drawStringCentered( sceneManager.italicsFont, "The End", videoManager.getScreenWidth()/2, 100 )
        videoManager.drawStringCentered( sceneManager.defaultFont, "By Jasper Van der Jeugt", videoManager.getScreenWidth()/2, 130 )
        videoManager.flip()
        sceneManager.waitForClick()
        mapManager.stop()

sceneManager.quitDialog()

# Remove people
thisMap.removeObject( esana )
thisMap.removeObject( inyse )
thisMap.removeObject( jelobat )
partyManager.refreshMap()

