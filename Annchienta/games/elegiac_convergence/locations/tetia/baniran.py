import annchienta, scene, party

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

baniran = annchienta.getPassiveObject()
player = partyManager.player
esana = annchienta.Person( "esana", "locations/prison/esana.xml" )

sceneManager.initDialog( [baniran, player, esana] )

pp = player.getPosition().to( annchienta.IsometricPoint )
bp = baniran.getPosition().to( annchienta.IsometricPoint )
ep = annchienta.Point( annchienta.IsometricPoint, pp.x + (30 if bp.x < pp.x else -30), pp.y )

esana.setPosition( pp )
partyManager.currentMap.addObject( esana )
sceneManager.move( esana, ep )

esana.lookAt( baniran )
player.lookAt( baniran )

if not partyManager.hasRecord("tetia_met_baniran"):

    partyManager.addRecord("tetia_met_baniran")
    sceneManager.speak( baniran, "Aelaan! What the heck have you been doing?" )
    sceneManager.chat( esana, "Do you know this lad?", ["Sure, our hideout is in Tetia. I know pretty much everyone here."] )
    sceneManager.speak( baniran, "I heard you were arrested for murder. I'm glad to see you back. I knew they were wrong, you wouldn't do anything so cruel." )
    a = sceneManager.chat( baniran, "So, how did they find out you were innocent?", ["Well, actually they didn't...", "I had an alibi."] )
    if a==0:
        sceneManager.chat( baniran, "What? You escaped? How did you manage to do that?", ["I couldn't do that on my own, Esana helped me out."] )
    else:
        sceneManager.chat( baniran, "I see. So, who is this lovely girl you brought with you?", ["That's Esana."] )

    sceneManager.speak( baniran, "Esana? Aren't you the daughter of Bardolph? I'm sorry for you father. Is there anything I can do?" )
    sceneManager.speak( esana, "Thanks... But I don't think you can help us... unless you have any idea on who really killed my father?" )
    sceneManager.speak( baniran, "No, I'm sorry." )

sceneManager.speak( baniran, "Why don't you sit here for a while and enjoy the sun?" )
partyManager.heal()
sceneManager.info( "Your health was restored.", None )

sceneManager.move( esana, pp )
sceneManager.quitDialog()
partyManager.currentMap.removeObject( esana )
