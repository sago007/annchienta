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
    a = sceneManager.chat( baniran, "So, how did they find out you were innocent?", ["Well, actually they didn't...", "They found the real murderer later."] )
    if a==0:
        pass
    else:
        pass

else:
    pass


sceneManager.move( esana, pp )
sceneManager.quitDialog()
partyManager.currentMap.removeObject( esana )
