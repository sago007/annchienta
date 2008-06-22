import annchienta, party, scene

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

player = partyManager.player
bardolph = partyManager.currentMap.getObject("bardolph")
kator = partyManager.currentMap.getObject("kator")

sceneManager.initDialog( [player, bardolph, kator] )

kator.lookAt( bardolph )

sceneManager.speak( kator, "Aelaan, help me!" )
sceneManager.speak( bardolph, "Stay away! I don't know what he told you, but this man is an assassin!" )
sceneManager.speak( kator, "I... what? You don't believe that, Aelaan, do you?" )
sceneManager.speak( bardolph, "Don't listen to him! Stay out of this!" )
sceneManager.speak( kator, "Trust me, Aelaan! We'll get through this!" )

pos = player.getPosition().to( annchienta.IsometricPoint )
pos.x += 30

sceneManager.move( player, pos )

sceneManager.quitDialog()

# Now change the map again, we're back on the ship
partyManager.changeMap( "locations/anpere/ship.xml", annchienta.Point( annchienta.TilePoint, 13, 7 ) )

