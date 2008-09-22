import annchienta, PartyManager, BattleManager

partyManager = PartyManager.getPartyManager()
battleManager = BattleManager.getBattleManager()
annchienta.getAudioManager().playMusic( "music/facilities.ogg")
annchienta.getVideoManager().setClearColor(147,201,233)
battleManager.enemiesInMap = ["brainfuck mutant"]
battleManager.background = "images/backgrounds/facilities.png"

