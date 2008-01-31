import annchienta

#videoMgr = annchienta.getVideoManager()
#videoMgr.setVideoMode( 400, 300, "Annchienta", False )

#inputMgr = annchienta.getInputManager()

#mapMgr = annchienta.getMapManager()
#mapMgr.setTileWidth(64)
#mapMgr.setTileHeight(32)

#mymap = annchienta.Map( "tileset/" )

#mapMgr.setCurrentMap( mymap )

#mapMgr.run()

mapMgr = annchienta.getMapManager()
mapMgr.setTileWidth(64)
mapMgr.setTileHeight(32)
editor = annchienta.Editor( "tileset/" )
editor.run()
