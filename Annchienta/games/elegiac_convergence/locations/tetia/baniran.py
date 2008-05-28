import annchienta, scene, party

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

# If we have inyse or not.
inyseInParty = partyManager.hasRecord("tetia_met_inyse")

baniran = annchienta.getPassiveObject()
player = partyManager.player
esana = annchienta.Person( "esana", "locations/prison/esana.xml" )
inyse = 0
if inyseInParty:
    inyse = annchienta.Person( "inyse", "locations/tetia/inyse.xml" )

sceneManager.initDialog( [baniran, player, esana] + ([inyse] if inyseInParty else []) )

pp = player.getPosition().to( annchienta.IsometricPoint )
bp = baniran.getPosition().to( annchienta.IsometricPoint )
ep = annchienta.Point( annchienta.IsometricPoint, pp.x + (30 if bp.x < pp.x else -30), pp.y )
ip = annchienta.Point( annchienta.IsometricPoint, pp.x, pp.y+30 )

esana.setPosition( pp )
partyManager.currentMap.addObject( esana )
sceneManager.move( esana, ep )
if inyseInParty:
    inyse.setPosition( pp )
    partyManager.currentMap.addObject( inyse )
    sceneManager.move( inyse, ip )

esana.lookAt( baniran )
player.lookAt( baniran )

if not partyManager.hasRecord("tetia_met_baniran"):

    partyManager.addRecord("tetia_met_baniran")
    sceneManager.speak( baniran, "Aelaan! What the heck have you been doing?" )
    sceneManager.chat( esana, "Do you know this guy?", ["Sure, our hideout is in Tetia. I know pretty much everyone here."] )
    sceneManager.speak( baniran, "I heard you were arrested for murder. I'm glad to see you back. I knew they were wrong, you wouldn't do anything so cruel." )
    a = sceneManager.chat( baniran, "So, how did they find out you were innocent?", ["Well, actually they didn't...", "I had an alibi."] )
    if a==0:
        sceneManager.chat( baniran, "What? You escaped? How did you manage to do that?", ["I couldn't do that on my own, Esana helped me out."] )
    else:
        sceneManager.chat( baniran, "I see. So, who is this lovely girl you brought with you?", ["That's Esana."] )

    sceneManager.speak( baniran, "Esana? Aren't you the daughter of Bardolph? I'm sorry for you father. Is there anything I can do?" )
    sceneManager.speak( esana, "Thanks... But I don't think you can help us... unless you have any idea on who really killed my father?" )
    sceneManager.speak( baniran, "No, I'm sorry." )

elif partyManager.hasRecord("tetia_met_inyse"):

    partyManager.addRecord("tetia_baniran_clues")
    sceneManager.speak( baniran, "Inyse! Long time no see... how've you been doing?" )
    sceneManager.speak( inyse, "..." )
    sceneManager.chat( baniran, "Is something wrong?", ["She just heard Cristopher died and..."] )
    sceneManager.chat( baniran, "Damn... what is happening lately? So many people dying, this attack...", ["That's what we're trying to find out."] )
    sceneManager.speak( inyse, "Why was I even attacked?" )
    sceneManager.speak( esana, "Unless they knew we were coming." )
    sceneManager.speak( inyse, "And who is able to tame ghosts anyway?" )
    sceneManager.speak( player, "He..." )
    sceneManager.speak( esana, "He? What?" )
    sceneManager.speak( player, "I just realised... It could've been... I mean, I'm not sure, but..." )
    inyse.lookAt( player )
    sceneManager.speak( inyse, "Say it already!" )
    sceneManager.speak( player, "Well, I've been thinking... This Jelobat was really good with beasts..." )
    sceneManager.chat( inyse, "The one who informed you about where you could find the pendant?", ["Yeah, that's the one."] )
    sceneManager.speak( inyse, "Hmm... If that is so, he was also the one who killed Esana's father once." )
    sceneManager.chat( esana, "Of course! Everything makes sense now!", ["And that means I'm innocent."] )
    sceneManager.speak( inyse, "We have to find him first, though. Any idea of where he might be?" )
    sceneManager.speak( player, "He's from Aldwar, an large island to the north. I suspect he'll try to return there." )
    sceneManager.speak( esana ,"I've been with to Aldwar with my father. He had to go there for negotiations with that island's governour." )
    sceneManager.speak( esana, "That island is huge, and there's a large jungle to the east. If he gets there... we'll probably never find him." )
    sceneManager.speak( inyse, "So we stop him. If he's heading there, our best chance is to head to Anpere." )
    sceneManager.speak( player, "Anpere is this island's only port, situated to the south... We have to head through the Tasumian woods to get there. Let's go." )

    sceneManager.text( "END OF ANNCHIENTA DEMO. THANKS FOR PLAYING." )

sceneManager.speak( baniran, "Why don't you sit here for a while and enjoy the sun?" )
partyManager.heal()
sceneManager.info( "Your health was restored.", None )

if inyseInParty:
    sceneManager.move( inyse, pp )

sceneManager.move( esana, pp )
sceneManager.quitDialog()
partyManager.currentMap.removeObject( esana )
if inyseInParty:
    partyManager.currentMap.removeObject( inyse )
