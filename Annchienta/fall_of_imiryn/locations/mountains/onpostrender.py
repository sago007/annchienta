import annchienta

videoManager = annchienta.getVideoManager()
cacheManager = annchienta.getCacheManager()
mapManager = annchienta.getMapManager()

surf = cacheManager.getSurface( "images/backgrounds/snow.png" )
p = engine.getTicks()/7
p %= videoManager.getScreenHeight()

videoManager.push()

#videoManager.translate( 0, p )

videoManager.translate( -(mapManager.getCameraX()%videoManager.getScreenWidth()), -((mapManager.getCameraY()-p)%videoManager.getScreenHeight()) )

videoManager.drawPattern( surf, 0, 0, videoManager.getScreenWidth()*2, videoManager.getScreenHeight()*2 )

videoManager.pop()

