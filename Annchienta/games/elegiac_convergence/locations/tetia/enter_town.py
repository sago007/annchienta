import annchienta, scene, party

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

player = annchienta.getActiveObject()
esana = annchienta.Person( "esana", "locations/prison/esana.xml" )

sceneManager.initDialog( [player, esana] )
pp = player.getPosition().to( annchienta.IsometricPoint )
esana.setPosition( pp )

partyManager.currentMap.addObject( esana )
pp.y += 30
sceneManager.move( esana, pp )

esana.lookAt( player )
player.lookAt( esana )

sceneManager.chat( esana, "I'm glad we made it this far. Still, we have to go on and find the killer.", ["Are you serious?"] )
sceneManager.speak( player, "It's a miracle we even made it this far. We need to hide..." )
sceneManager.chat( esana, "Have you forgotten about my father? I will not be able to rest until the killer is in prison!", ["I'm sorry."] )
sceneManager.chat( esana, "I'm going to find out who cut my father's head off. I'm going to retrieve it and give him a proper burial. Are you with me?", ["You set me free, so I guess..."] )
sceneManager.chat( esana, "Exactly... now, where do we begin our search...", ["I know this town pretty well... our hideout is situated here."] )
sceneManager.chat( esana, "The hideout of your bandit club?", ["If that's how you refer to it, yes."] )
sceneManager.speak( esana, "Allright, we start our search there. Let's go." )

sceneManager.thoughts( "What did I get myself into now? Looking for the head of the father of a girl way out of my league..." )

pp.y -= 30

sceneManager.move( esana, pp )
sceneManager.quitDialog()
partyManager.currentMap.removeObject( esana )

partyManager.addRecord("tetia_entered_town")
partyManager.refreshMap()
