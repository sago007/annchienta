import annchienta, PartyManager

partyManager = PartyManager.getPartyManager()
annchienta.getAudioManager().playMusic( "music/mountains.ogg")
annchienta.getVideoManager().setClearColor(147,201,233)
partyManager.enemiesInMap = ["ice warrior", "coeurl"]
partyManager.background = "images/backgrounds/ice.png"

# Load images we need for rendering into the cache
# so we don't have to do this on-the-fly.
cacheManager = annchienta.getCacheManager()
cacheManager.getSurface( "images/backgrounds/mountains.png" )
cacheManager.getSurface( "images/backgrounds/snow.png" )
