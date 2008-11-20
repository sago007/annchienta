import annchienta, PartyManager, BattleManager

partyManager = PartyManager.getPartyManager()
battleManager = BattleManager.getBattleManager()
annchienta.getAudioManager().playMusic( "music/inaran.ogg")
annchienta.getVideoManager().setClearColor(60,60,60)
battleManager.enemiesInMap = ["goblin", "stauld", "squid"]
battleManager.background = "images/backgrounds/cave.png"

