import annchienta, PartyManager, BattleManager

partyManager = PartyManager.getPartyManager()
battleManager = BattleManager.getBattleManager()
annchienta.getAudioManager().playMusic( "music/mountains.ogg")
annchienta.getVideoManager().setClearColor(147,201,233)
battleManager.setRandomBattleEnemies( ["ice warrior", "coeurl", "hawk"] )
battleManager.setRandomBattleBackground( "images/backgrounds/ice.png" )

# Load images we need for rendering into the cache
# so we don't have to do this on-the-fly.
cacheManager = annchienta.getCacheManager()
cacheManager.getSurface( "images/backgrounds/mountains.png" )
cacheManager.getSurface( "images/backgrounds/snow.png" )
