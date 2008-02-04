import annchienta
import time

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
audioMgr.playMusic( "maps/drum_intro.ogg" )

player = [ annchienta.Surface("maps/persontest.png"), annchienta.Surface("maps/persontest2.png") ]
sprite = 0
x = 0
y = 0

while inputMgr.running():
    inputMgr.update()
    mapMgr.renderFrame()
    videoMgr.drawSurface( player[sprite], x, y )
    videoMgr.flip()
    sprite = (sprite+1)%2
    x += 2
    y += 1
    time.sleep(0.5)
