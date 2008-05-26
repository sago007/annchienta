import annchienta, scene, party

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

inyse = partyManager.currentMap.getObject("inyse")
player = partyManager.player
esana = annchienta.Person( "esana", "locations/prison/esana.xml" )
esana.setPosition( annchienta.Point( annchienta.TilePoint, 7, 2 ) )

sceneManager.initDialog( [inyse, player, esana] )

player.lookAt( inyse )
esana.lookAt( inyse )

sceneManager.speak( inyse, "Aelaan! You returned! Where is Cristopher? I want to see him!" )

sceneManager.quitDialog()
partyManager.currentMap.removeObject( esana )

partyManager.addRecord("tetia_met_inyse")
partyManager.refreshMap()
