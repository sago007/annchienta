import annchienta

videoMgr = annchienta.getVideoManager()
videoMgr.setVideoMode( 400, 300, "Annchienta", False )

inputMgr = annchienta.getInputManager()

mapMgr = annchienta.getMapManager()
mapMgr.setTileWidth(64)
mapMgr.setTileHeight(32)

mymap = annchienta.Map( "tileset/" )

while inputMgr.running():
    
    inputMgr.update()
    
    if( inputMgr.keyDown( annchienta.SDLK_LEFT ) ):
        videoMgr.translate( 1, 0 )
    if( inputMgr.keyDown( annchienta.SDLK_RIGHT ) ):
        videoMgr.translate( -1, 0 )
    if( inputMgr.keyDown( annchienta.SDLK_UP ) ):
        videoMgr.translate( 0, 1 )
    if( inputMgr.keyDown( annchienta.SDLK_DOWN ) ):
        videoMgr.translate( 0, -1 )
    
    mymap.depthSort()
    mymap.draw()
    
    videoMgr.flip()
    