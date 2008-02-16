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
sceneMgr.defaultFont = annchienta.Font("assets/font.ttf", 16)

for i in range(9):
    sceneMgr.boxTextures.append( annchienta.Surface("assets/box"+str(i)+".png") )

#while inputMgr.running():
    ##mapMgr.renderFrame()
    #videoMgr.setColor(255,0,0,200)
    #videoMgr.drawRectangle(0,0,400,300)
    #videoMgr.setColor()
    #sceneMgr.text( "Lorem ipsum dolor sit amet!\nConsectetuer adipiscing elit. Phasellus purus nisl, laoreet id, ornare nec, bibendum at, velit. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer sapien. Nullam eleifend, ligula pharetra mattis tincidunt, sem nibh aliquet purus, quis ullamcorper ligula eros nec risus. Sed posuere turpis id elit fringilla imperdiet. Donec massa felis, venenatis quis, elementum tempor, cursus at, dui. Sed placerat enim vitae dolor. Morbi nunc justo, sollicitudin eget, tincidunt sit amet, interdum in, leo. Vestibulum dolor ipsum, fermentum vel, dapibus quis, consequat et, nulla. Nam pede neque, convallis et, porttitor nec, dictum nec, libero." )
    #inputMgr.update()
    #videoMgr.flip()
mapMgr.run()
