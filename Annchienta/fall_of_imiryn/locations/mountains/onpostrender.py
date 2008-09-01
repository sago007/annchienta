import annchienta

videoManager = annchienta.getVideoManager()
cacheManager = annchienta.getCacheManager()
mapManager = annchienta.getMapManager()

surf = cacheManager.getSurface( "images/backgrounds/snow.png" )
p = engine.getTicks()/7
p %= videoManager.getScreenHeight()

videoManager.pushMatrix()

#videoManager.translate( 0, p )

videoManager.translate( -(mapManager.getCameraX()%videoManager.getScreenWidth()), -((mapManager.getCameraY()-p)%videoManager.getScreenHeight()) )

videoManager.drawSurface( surf, 0, 0 )
videoManager.drawSurface( surf, videoManager.getScreenWidth(), 0 )
videoManager.drawSurface( surf, videoManager.getScreenWidth(), videoManager.getScreenHeight() )
videoManager.drawSurface( surf, 0, videoManager.getScreenHeight() )

videoManager.popMatrix()

