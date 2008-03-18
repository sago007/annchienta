import annchienta
import scene
import party

videoMgr = annchienta.getVideoManager()
videoMgr.setVideoMode( 400, 300, "Annchienta", False )

mapMgr = annchienta.getMapManager()
mapMgr.setTileWidth(64)
mapMgr.setTileHeight(32)
mapMgr.setUpdatesPerSecond(60)
mapMgr.setMaxAscentHeight(32)
mapMgr.setMaxDescentHeight(32)

scene.initSceneManager()
sceneMgr = scene.getSceneManager()
sceneMgr.defaultFont = annchienta.Font("assets/font.ttf", 14)

for i in range(9):
    sceneMgr.boxTextures.append( annchienta.Surface("assets/box"+str(i)+".png") )

party.initPartyManager()
partyManager = party.getPartyManager()
partyManager.load("save.xml")

mapMgr.run()
