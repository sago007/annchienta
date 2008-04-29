import annchienta
import scene
import party

engine = annchienta.getEngine()
mapManager = annchienta.getMapManager()
inputManager = annchienta.getInputManager()
sceneManager = scene.getSceneManager()
partyManager = party.getPartyManager()

active = annchienta.getActiveObject()
passive = annchienta.getPassiveObject()

# The name of the passive object.
passiveName = "nameless"
if "getName" in dir(passive):
    passiveName = passive.getName().lower()

player = partyManager.player

# The first event
if not partyManager.hasRecord("prison_awakening"):
    partyManager.addRecord("prison_awakening")
    player.setPosition( annchienta.Point( annchienta.TilePoint, 8, 5 ) )
    sceneManager.initDialog( [player] )
    sceneManager.thoughts( "Ouch..." )
    sceneManager.thoughts( "My head is all fuzzy-like..." )
    sceneManager.speak( player, "Where the heck am I?" )
    sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 8, 2 ) )
    sceneManager.speak( player, "This can't be prison?" )
    sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 9, 2 ) )
    sceneManager.speak( player, "And why... Why can't I remember anything?" )
    sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 7, 2 ) )
    sceneManager.speak( player, "What the heck is going on?" )
    sceneManager.thoughts( "Last thing I remember..." )
    sceneManager.thoughts( "We were on a mission... It had something to do with stealing something... It... it can't be, they never could've caught us..."  )
    sceneManager.thoughts( "I can still recall we entered the building... Yeah, this Jelobat lead us is through a hidden passage... We were there to steal something... a pendant, I think." )
    sceneManager.thoughts( "Where is the rest? Where are Christopher and Vincent? And where is Jelobat?" )
    sceneManager.thoughts( "We entered the building, and then we..." )
    sceneManager.noise()
    sceneManager.thoughts( "Ouch... Why can't I remember?" )
    sceneManager.speak( player, "Why can't I remember?!" )
    sceneManager.speak( player, "I need to find out what happened... I must find the others! I must speak to them!" )
    sceneManager.info( "Use the arrow keys to move.", None )
    sceneManager.info( "Press spacebar to inspect items.", None )
    sceneManager.quitDialog()
    partyManager.refreshMap()

# The event with the guard.
if partyManager.hasRecord("prison_awakening") and not partyManager.hasRecord("prison_guard") and passiveName=="bars":

    partyManager.addRecord("prison_guard")

    # Create a guard and set his position.
    guard = annchienta.Person( "guard", "locations/prison/guard.xml" )
    partyManager.currentMap.addObject( guard )
    guard.setPosition( annchienta.Point( annchienta.IsometricPoint, 30, 140 ) )

    # Init the dialog.
    sceneManager.initDialog( [guard, player] )

    # Follow the guard walking to Aelaan.
    p = player.getPosition().to( annchienta.IsometricPoint )
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 30, p.y ) )
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 74, p.y ) )
    guard.lookAt( player )
    player.lookAt( guard )

    # Chat a little.
    sceneManager.chat( guard, "What's all that noise? Did our precious newcomer wake up at last?.", ["Let me out of here!"] )
    sceneManager.chat( guard, "Letting you out?! You've got to be kidding! You're the cruelest murderer we've ever had down here.", ["How.. what!?"] )
    sceneManager.chat( guard, "So you are indeed suffering from amnesia. The doctor told us something like that could happen.", ["The doctor?"] )
    sceneManager.chat( guard, "Yeah, they called a doctor to look after your head injury. Pretty much a waste of time, since you are going to be executed very soon anyway.", ["Executed? Why!?"] )
    sceneManager.speak( guard, "Maybe for breaking into the house of this island's governour Bardolph. Maybe for murdering his two loyal bodyguards. Or wait, maybe for killing the governour himself and cutting his head off?" )
    sceneManager.speak( guard, "You are a monster, I hope you realise that. I hope his family will have some rest when they hear you will receive death penalty." )

    sceneManager.thoughts("I... I can't have...")

    # Guard backs off, but returns.
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 40, p.y ) )
    sceneManager.speak( player, "Wait!" )
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 74, p.y ) )

    # Keep talking.
    sceneManager.chat( guard, "What is it this time?", ["You've got to let me out!"] )
    sceneManager.chat( guard, "I really don't see any reason why I should free a murderer like you.", ["But I'm innocent!"] )
    sceneManager.chat( guard, "You were found unconsciously on the crime scene, with the murder weapon in your hands!", ["But I can't have... was there nobody else?"] )
    sceneManager.speak( guard, "Well, no, not alive. Except from the bodyguards, some other bodies were found, too. It makes no sense denying that they were with you." )
    sceneManager.speak( guard, "Now that the verdict has been spoken, you will be executed within twenty four hours." )

    # The guard walks back as he came in.
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 30, p.y ) )
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 30, 140 ) )

    # Some more thoughts after the scene.
    sceneManager.speak( player, "Not alive... I..." )
    sceneManager.thoughts( "Cristopher... Vincent... Jelobat... dead? " )
    sceneManager.thoughts( "Could that guard be speaking the truth? I... I don't feel like a murderer... I'm just a thief... a horribly failed thief!")
    sceneManager.thoughts( "I've got to get out!" )

    # Remove the guard.
    sceneManager.quitDialog()
    partyManager.currentMap.removeObject( guard )
    partyManager.refreshMap()

# The event with Esana.
if partyManager.hasRecord("prison_guard") and not partyManager.hasRecord("prison_met_esana") and passiveName=="bed":

    partyManager.addRecord("prison_met_esana")

    # Create Esana and set her position.
    esana = annchienta.Person( "esana", "locations/prison/esana.xml" )
    partyManager.currentMap.addObject( esana )
    esana.setPosition( annchienta.Point( annchienta.IsometricPoint, 30, 140 ) )

    # Init the dialog.
    sceneManager.initDialog( [esana, player] )

    # Esana walks to the gate.
    sceneManager.move( esana, annchienta.Point( annchienta.IsometricPoint, 30, 40 ) )
    sceneManager.move( esana, annchienta.Point( annchienta.IsometricPoint, 74, 40 ) )
    player.lookAt(esana)

    # Esana opens the gate.
    bar = 1
    while bar:
        bar = partyManager.currentMap.getObject("bars")
        if bar:
            partyManager.currentMap.removeObject(bar)

    mapManager.renderFrame()

    sceneManager.speak( esana, "I know someone who's got to take better care of his keys." )

    # Esana walks to the player
    p = player.getPosition().to( annchienta.IsometricPoint )
    sceneManager.move( esana, annchienta.Point( annchienta.IsometricPoint, p.x-20, 40 ) )
    sceneManager.move( esana, annchienta.Point( annchienta.IsometricPoint, p.x-20, p.y ) )
    esana.lookAt( player )

    sceneManager.chat( esana, "Come on, let's go! What are you waiting for?", ["Who...? Are you... Esana? You here?"] )
    sceneManager.speak( esana, "It's been a long time, yeah, but we'll catch up later. We need to get going now. Come on, follow." )

    sceneManager.move( esana, annchienta.Point( annchienta.IsometricPoint, p.x-40, p.y ) )

    sceneManager.speak( player, "Esana, wait. Bardolph, your father... I didn't... I didn't mean too... I don't know..." )
    sceneManager.speak( esana, "Don't get silly, I know as well as you do that you're innocent. Now let's get moving." )

    sceneManager.move( esana, annchienta.Point( annchienta.IsometricPoint, p.x, p.y ) )

    # Remove Esana.
    sceneManager.quitDialog()
    partyManager.currentMap.removeObject( esana )

    mapManager.renderFrame()
    sceneManager.info( "Esana joined the party.", None )

    partyManager.refreshMap()

if partyManager.hasRecord("prison_met_esana") and not partyManager.hasRecord("prison_through_window") and passiveName=="nameless":

    partyManager.addRecord("prison_through_window")

    # Create Esana and set her position.
    esana = annchienta.Person( "esana", "locations/prison/esana.xml" )
    partyManager.currentMap.addObject( esana )
    p = player.getPosition()
    esana.setPosition( p )

    # Init the dialog.
    sceneManager.initDialog( [esana, player] )

    p.x = p.x+30

    # Esana moves away a little.
    sceneManager.move( esana, p )
    player.lookAt(esana)
    esana.lookAt(player)

    # Talk a little, then move back.
    sceneManager.chat( esana, "Yeah, we actually have to go down that window.", ["What?"] )
    sceneManager.speak( esana, "Below us are only guards. And I brought this rope just in case... Let's go!" )
    sceneManager.move( esana, player.getPosition() )

    # Remove Esana.
    sceneManager.quitDialog()
    partyManager.currentMap.removeObject( esana )

    background = annchienta.Surface( "images/storyline/prison_tower.png" )
    s1 = annchienta.Surface( "sprites/aelaan.png" )
    s2 = annchienta.Surface( "sprites/esana.png" )
    start = engine.getTicks()
    while start+9000>engine.getTicks() and inputManager.running():
        inputManager.update()
        t = engine.getTicks()-start
        videoManager.begin()
        videoManager.translate( 0, (-engine.getTicks()+start)/10 )
        videoManager.drawPattern( background, 0, 0, 400, 1200 )
        videoManager.drawSurface( s1, 142, 600, 0, 0, 37, 75 )
        videoManager.drawSurface( s2, 142, 680, 0, 0, 31, 71 )
        videoManager.end()

    videoManager.reset()
    f = annchienta.Font( "assets/italics.ttf", 40 )
    videoManager.setColor(0,0,0,200)
    videoManager.drawRectangle(0,0,videoManager.getScreenWidth(),videoManager.getScreenHeight())
    videoManager.setColor(255,255,255)
    videoManager.drawStringCentered( sceneManager.defaultFont, "And all was well.", 200, 80 )
    videoManager.drawStringCentered( f, "The End.", 200, 100 )
    mapManager.stop()
    sceneManager.waitForKey()
    engine.write("Thanks for playing Annchienta.")
