import annchienta, scene, party, battle

partyManager = party.getPartyManager()
sceneManager = scene.getSceneManager()

passiveObject = annchienta.getPassiveObject()

# Fight with wolf here.
audioManager.playMusic( "music/battle_3.ogg" )

# Create some enemies
enemies = [battle.getBattleManager().createEnemy("wolf")]

# Start a battle.
b = battle.Battle( partyManager.team + enemies )
b.background = annchienta.Surface("images/backgrounds/woods.png")
b.run()

if b.won:
    partyManager.addRecord( "tasumian_killed_"+passiveObject.getName() )
    partyManager.refreshMap()
