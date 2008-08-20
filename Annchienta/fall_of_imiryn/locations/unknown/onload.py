import annchienta, PartyManager

partyManager = PartyManager.getPartyManager()
annchienta.getAudioManager().playMusic( "music/unknown.ogg")
annchienta.getVideoManager().setClearColor(147,201,233)
partyManager.enemiesInMap = ["spider", "worm", "ghost"]
partyManager.background = "images/backgrounds/grass.png"

