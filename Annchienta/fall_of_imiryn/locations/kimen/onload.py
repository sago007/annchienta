import annchienta, PartyManager, BattleManager

partyManager = PartyManager.getPartyManager()
battleManager = BattleManager.getBattleManager()
annchienta.getAudioManager().playMusic( "music/kimen.ogg")
annchienta.getVideoManager().setClearColor(147,201,233)
battleManager.setRandomBattleEnemies( ["captain", "dragon", "war mage"] )
battleManager.setRandomBattleBackground( "images/backgrounds/kimen.png" )

