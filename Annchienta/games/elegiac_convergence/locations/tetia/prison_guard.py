import scene
import annchienta
import party

mapManager = annchienta.getMapManager()
sceneManager = scene.getSceneManager()
partyManager = party.getPartyManager()

player = partyManager.player

# We only want this even on certain record conditions.
if partyManager.hasRecord("tetia_prison_awakening") and not partyManager.hasRecord("tetia_prison_guard"):

    partyManager.addRecord("tetia_prison_guard")

    # Create a guard and set his position.
    guard = annchienta.Person( "guard", "locations/tetia/prison_guard.xml" )
    partyManager.currentMap.addObject( guard )
    guard.setPosition( annchienta.Point( annchienta.IsometricPoint, 30, 140 ) )

    # Follow the guard walking to Aelaan.
    p = player.getPosition().to( annchienta.IsometricPoint )
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 30, p.y ) )
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 74, p.y ) )

    # Init the dialog.
    sceneManager.initDialog( [guard, player] )

    # Chat a little.
    sceneManager.chat( guard, "I see our newcomer finally woke up.", ["Let me out of here!"] )
    sceneManager.chat( guard, "I'm afraid I cannot do that. You did something terrible, and therefore you should face the consequences!", ["How.. what did I do?"] )
    sceneManager.chat( guard, "Don't play stupid with me, I know your kind.", ["But I can't remember, I really can't!"] )
    sceneManager.chat( guard, "Well then, you are sentenced to death because of murder. Rings any bells?", ["What?!"] )

    # Guard backs off, but returns.
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 40, p.y ) )
    sceneManager.speak( player, "Wait!" )
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 74, p.y ) )

    # Keep talking.
    sceneManager.chat( guard, "What is it this time?", ["You've got to let me out!"] )
    sceneManager.chat( guard, "I really don't see any reason why I should free a murderer like you.", ["But I'm innocent!"] )
    sceneManager.chat( guard, "You were found unconsciously on the crime scene, with the weapon of murder in your hands!", ["But I can't have... was there nobody else?"] )
    sceneManager.speak( guard, "Well, no, not alive. Now that the verdict has been spoken, you will be executed within twenty four hours." )

    # The guard walks back as he came in.
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 30, p.y ) )
    sceneManager.move( guard, annchienta.Point( annchienta.IsometricPoint, 30, 140 ) )

    # Some more thoughts after the scene.
    sceneManager.speak( player, "Not alive..." )
    sceneManager.thoughts( "Not alive..." )
    sceneManager.thoughts( "Could that guard be speaking the truth? I... I don't feel like a murderer... I'm just a thief... a failed thief!")
    sceneManager.thoughts( "I've got to get out!" )

    # Remove the guard.
    sceneManager.quitDialog()
    partyManager.currentMap.removeObject( guard )
