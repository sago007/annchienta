import annchienta

videoManager = annchienta.getVideoManager()
cacheManager = annchienta.getCacheManager()

surf = cacheManager.getSurface( "images/backgrounds/mountains.png" )
videoManager.drawSurface( surf, 0, 0 )

