import annchienta
from scene import *

videoMgr = annchienta.getVideoManager()
videoMgr.setVideoMode( 400, 300, "Annchienta", False )

inputMgr = annchienta.getInputManager()

mapMgr = annchienta.getMapManager()
mapMgr.setTileWidth(64)
mapMgr.setTileHeight(32)
mapMgr.setUpdatesPerSecond(60)
mapMgr.setMaxAscentHeight(16)
mapMgr.setMaxDescentHeight(32)

mymap = annchienta.Map( "maps/map.xml" )

mapMgr.setCurrentMap( mymap )

initSceneManager()
sceneMgr = getSceneManager()
sceneMgr.defaultFont = annchienta.Font("assets/font.ttf", 14)

for i in range(9):
    sceneMgr.boxTextures.append( annchienta.Surface("assets/box"+str(i)+".png") )

mapMgr.run()
