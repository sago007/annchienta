import annchienta

videoMgr = annchienta.getVideoManager()
videoMgr.setVideoMode( 400, 300, "Annchienta", False )

inputMgr = annchienta.getInputManager()

mapMgr = annchienta.getMapManager()
mapMgr.setTileWidth(64)
mapMgr.setTileHeight(32)

mymap = annchienta.Map( "maps/map.xml" )
#mymap = annchienta.Map( 10, 10, "tileset/" )

mapMgr.setCurrentMap( mymap )

audioMgr = annchienta.getAudioManager()
sound = annchienta.Sound("maps/drum.ogg")
audioMgr.playSound( sound )

player = annchienta.Surface("maps/persontest.png")

while inputMgr.running():
    inputMgr.update()
    mapMgr.renderFrame()
    videoMgr.drawSurface( player, 10, 10 )
    videoMgr.flip()
    