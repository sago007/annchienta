import annchienta, PartyManager, BattleManager

partyManager = PartyManager.getPartyManager()
battleManager = BattleManager.getBattleManager()
annchienta.getAudioManager().playMusic( "music/kimen.ogg")
annchienta.getVideoManager().setClearColor(147,201,233)
battleManager.enemiesInMap = ["captain"]
battleManager.background = "images/backgrounds/kimen.png"

