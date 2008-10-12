import annchienta, PartyManager, BattleManager

partyManager = PartyManager.getPartyManager()
battleManager = BattleManager.getBattleManager()
annchienta.getAudioManager().playMusic( "music/unknown.ogg")
annchienta.getVideoManager().setClearColor(147,201,233)
battleManager.enemiesInMap = ["spider", "worm", "ghost"]
battleManager.background = "images/backgrounds/grass.png"

