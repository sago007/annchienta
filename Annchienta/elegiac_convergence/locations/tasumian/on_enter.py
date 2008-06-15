import annchienta, scene, party

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

# Create persons
player = partyManager.player
esana = annchienta.Person("esana", "locations/prison/esana.xml")
inyse = annchienta.Person("inyse", "locations/tetia/inyse.xml")

# Add them to the map
partyManager.currentMap.addObject( esana )
partyManager.currentMap.addObject( inyse )

# Find positions.
pp = player.getPosition().to( annchienta.IsometricPoint )
ip = annchienta.Point( annchienta.IsometricPoint, pp.x-30, pp.y )
ep = annchienta.Point( annchienta.IsometricPoint, pp.x+30, pp.y )

# Set positions.
esana.setPosition( pp )
inyse.setPosition( pp )
pp.y += 30

# Init and move to right positions.
sceneManager.initDialog( [player, esana, inyse] )
sceneManager.move( [player,esana,inyse], [pp,ep,ip] )

# Some dialog now.
sceneManager.speak( esana, "I really can't believe we're doing this." )
sceneManager.speak( inyse, "There's no other way, they'd be expecting us on the road." )
sceneManager.speak( player, "Besides, these woods can't be that dangerous, can they?" )
sceneManager.speak( esana, "I read they were never the same, always changing..." )
sceneManager.speak( inyse, "I don't know... things just aren't what they seem here, I think." )
sceneManager.speak( player, "Let's continue... I mean, next week, we'll be laughing about this." )

# Stop dialog
sceneManager.fadeOut()
sceneManager.quitDialog()

partyManager.currentMap.removeObject( esana )
partyManager.currentMap.removeObject( inyse )
partyManager.addRecord("tasumian_entered_woods")
partyManager.refreshMap()
