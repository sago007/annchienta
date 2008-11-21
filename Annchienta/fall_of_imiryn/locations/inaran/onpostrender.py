import annchienta

videoManager = annchienta.getVideoManager()
cacheManager = annchienta.getCacheManager()
mapManager = annchienta.getMapManager()

surf = cacheManager.getSurface( "images/backgrounds/fog.png" )
p = engine.getTicks()/18
p %= videoManager.getScreenHeight()

videoManager.push()

videoManager.translate( -(mapManager.getCameraX()%videoManager.getScreenWidth()), -((mapManager.getCameraY()-p)%videoManager.getScreenHeight()) )

videoManager.drawPattern( surf, 0, 0, videoManager.getScreenWidth()*2, videoManager.getScreenHeight()*2 )

videoManager.pop()

