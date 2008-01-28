import annchienta

videoMgr = annchienta.getVideoManager()
videoMgr.setVideoMode( 400, 300, "Annchienta", False )

inputMgr = annchienta.getInputManager()

mapMgr = annchienta.getMapManager()
mapMgr.setTileWidth(64)
mapMgr.setTileHeight(32)

mymap = annchienta.Map( "../games/tileset/" )

while inputMgr.running():
    
    inputMgr.update()
    
    mymap.draw()
    
    videoMgr.flip()
    