import annchienta, party, scene

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

player = partyManager.player
bardolph = partyManager.currentMap.getObject("bardolph")
jelobat = partyManager.currentMap.getObject("jelobat")

sceneManager.initDialog( [player, bardolph, jelobat] )

jelobat.lookAt( bardolph )

sceneManager.speak( jelobat, "Aelaan, help me!" )
sceneManager.speak( bardolph, "Stay away! I don't know what he told you, but this man is an assassin!" )
sceneManager.speak( jelobat, "I... what? You don't believe that, Aelaan, do you?" )
sceneManager.speak( bardolph, "Don't listen to him! Stay out of this!" )
sceneManager.speak( jelobat, "Trust me, Aelaan! We'll get through this!" )

pos = player.getPosition().to( annchienta.IsometricPoint )
pos.x += 30

sceneManager.move( player, pos )

sceneManager.quitDialog()

# Now change the map again, we're back on the ship
partyManager.changeMap( "locations/anpere/ship.xml", annchienta.Point( annchienta.TilePoint, 13, 7 ) )

