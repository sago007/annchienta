import annchienta, scene, party
import combatant, xml.dom.minidom
import battle

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

# Add a combatant to the party.
document = xml.dom.minidom.parse( "locations/tetia/inyse_combatant.xml" )
e = document.getElementsByTagName("combatant")
comb = combatant.Ally( e[0] )
partyManager.team += [comb]

# Create some enemies
enemies = map( lambda a:battle.getBattleManager().createEnemy("ghost"), range(3) )

# Start a battle.
b = battle.Battle( partyManager.team + enemies )
b.background = annchienta.Surface("images/backgrounds/wooden_floor.png")
b.run()

sceneManager.quitDialog()
partyManager.currentMap.removeObject( esana )

partyManager.addRecord("tetia_met_inyse")
partyManager.refreshMap()
