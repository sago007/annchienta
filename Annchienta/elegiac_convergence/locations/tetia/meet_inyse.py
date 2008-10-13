import annchienta, scene, party
import combatant, xml.dom.minidom
import battle

mapManager = annchienta.getMapManager()
audioManager = annchienta.getAudioManager()
partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

inyse = partyManager.currentMap.getObject("inyse")
player = partyManager.player
esana = annchienta.Person( "esana", "locations/prison/esana.xml" )
esana.setPosition( annchienta.Point( annchienta.TilePoint, 7, 2 ) )
partyManager.currentMap.addObject( esana )

sceneManager.initDialog( [inyse, player, esana] )

player.lookAt( inyse )
esana.lookAt( inyse )

sceneManager.speak( player, "Inyse! What is happening?" )
sceneManager.speak( inyse, "Do I look like I know?" )
sceneManager.speak( player, "But who sent these? How did these ghosts get here?" )
sceneManager.speak( inyse, "I'm not sure, but apparently, someone who doesn't like us." )
sceneManager.speak( player, "Come on, Esana, we have to help! Inyse, are you alright?" )
sceneManager.speak( inyse, "Could've taken them on my own, but fine. Might have gotten nasty if one more had shown up." )

sceneManager.rotateEffect()

# Add a combatant to the party.
document = xml.dom.minidom.parse( "locations/tetia/inyse_combatant.xml" )
e = document.getElementsByTagName("combatant")
comb = combatant.Ally( e[0] )
partyManager.team += [comb]

audioManager.playMusic( "music/battle_2.ogg" )

gameOver = False

# Three similar battles.
for i in range(3):

    if mapManager.running():
        # Create some enemies
        enemies = map( lambda a:battle.getBattleManager().createEnemy("ghost"), range(3) )

        # Start a battle.
        b = battle.Battle( partyManager.team + enemies )
        b.background = annchienta.Surface("images/backgrounds/wooden_floor.png")
        b.run()
    else:
        gameOver = True

if not gameOver:
    # Remove the ghosts.
    for i in range(8):
        g = partyManager.currentMap.getObject( "ghost"+str(i+1) )
        partyManager.currentMap.removeObject( g )

    player.setPosition( annchienta.Point( annchienta.TilePoint, 5, 2 ) )
    sceneManager.move( player, annchienta.Point( annchienta.TilePoint, 5, 7 ) )

    sceneManager.speak( player, "Esana, this is Inyse. She's a member of our alliance. Inyse, this is Esana. We're searching for the murderer of her father." )

    sceneManager.move( esana, annchienta.Point( annchienta.TilePoint, 7, 7 ) )

    sceneManager.speak( inyse, "Hold on there. I was tracking down some wild beast when I heard something had gone wrong with you guys." )
    sceneManager.speak( inyse, "That's when I decided to head back to get information. But I was attacked as I entered our hideout..." )
    sceneManager.speak( inyse, "But I think I heard something about you guys being arrested? How is it possible that you're here, then? And where is Cristopher? I want to see him!" )
    sceneManager.speak( player, "Inyse... I don't know how to say this, but... Cristopher, he died..." )
    inyse.setAnimation( "standnorth" )
    sceneManager.speak( inyse, "He... can't have... he promised me we'd..." )
    inyse.setAnimation( "standeast" )
    sceneManager.speak( inyse, "I..." )
    sceneManager.speak( player, "I'm so sorry." )
    sceneManager.chat( inyse, "Who did this?", ["Well..."] )

    sceneManager.thoughts( "I told her what had happened, and how we were searching for the real murderer. She was determined to travel with us, wanting revenge on the man who murdered her love. Still, the question remained: who did all these terrible things?" )

    sceneManager.speak( player, "The one who did all this... who is it..." )
    sceneManager.speak( esana, "Could he, and the one who sent these ghosts at us, be one and the same?" )
    sceneManager.speak( inyse, "I believe so. We'd better ask around in town." )

    sceneManager.fadeOut()

sceneManager.quitDialog()
partyManager.currentMap.removeObject( esana )

if not gameOver:
    partyManager.addRecord("tetia_met_inyse")
    partyManager.refreshMap()
