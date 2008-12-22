import annchienta, PartyManager, BattleManager

partyManager = PartyManager.getPartyManager()
battleManager = BattleManager.getBattleManager()
annchienta.getAudioManager().playMusic( "music/facilities.ogg")
annchienta.getVideoManager().setClearColor(72,68,50)
battleManager.setRandomBattleEnemies( ["brainfuck mutant", "sample 0x4a", "soldier"] )
battleManager.setRandomBattleBackground( "images/backgrounds/facilities.png" )

