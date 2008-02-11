import annchienta
from scene import *

videoMgr = annchienta.getVideoManager()
videoMgr.setVideoMode( 400, 300, "Annchienta", False )

inputMgr = annchienta.getInputManager()

mapMgr = annchienta.getMapManager()
mapMgr.setTileWidth(64)
mapMgr.setTileHeight(32)
mapMgr.setUpdatesPerSecond(60)

mymap = annchienta.Map( "maps/map.xml" )
#mymap = annchienta.Map( 10, 10, "tileset/" )

mapMgr.setCurrentMap( mymap )

audioMgr = annchienta.getAudioManager()
audioMgr.playMusic( "maps/drum_intro.ogg" )

initSceneManager()
sceneMgr = getSceneManager()

while inputMgr.running():
    #mapMgr.renderFrame()
    sceneMgr.text( "Lorem ipsum dolor sit amet!\nConsectetuer adipiscing elit. Phasellus purus nisl, laoreet id, ornare nec, bibendum at, velit. Lorem ipsum dolor sit amet, consectetuer adipiscing elit." )
    inputMgr.update()
    videoMgr.flip()
#mapMgr.run()
