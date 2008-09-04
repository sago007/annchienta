import annchienta, PartyManager

partyManager = PartyManager.getPartyManager()
annchienta.getAudioManager().playMusic( "music/inaran.ogg")
annchienta.getVideoManager().setClearColor(0,0,0)
partyManager.enemiesInMap = ["goblin", "stauld", "squid"]
partyManager.background = "images/backgrounds/cave.png"
