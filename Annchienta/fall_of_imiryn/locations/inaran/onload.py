import annchienta, PartyManager, BattleManager

partyManager = PartyManager.getPartyManager()
battleManager = BattleManager.getBattleManager()
annchienta.getAudioManager().playMusic( "music/inaran.ogg")
annchienta.getVideoManager().setClearColor(0,0,0)
battleManager.enemiesInMap = ["goblin", "stauld", "squid"]
battleManager.background = "images/backgrounds/cave.png"

