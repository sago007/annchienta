import sys

# Add the scripts directory to the path so we can
# import modules from it.
sys.path.append("scripts")

import annchienta

videoMgr = annchienta.getVideoManager()
videoMgr.setVideoMode( 400, 300, "Annchienta", False )

mapMgr = annchienta.getMapManager()
mapMgr.setTileWidth(64)
mapMgr.setTileHeight(32)
mapMgr.setUpdatesPerSecond(60)
mapMgr.setMaxAscentHeight(32)
mapMgr.setMaxDescentHeight(32)
mapMgr.setOnUpdateScript("scripts/onupdate.py")

inputMgr = annchienta.getInputManager()
inputMgr.setInteractKey( annchienta.SDLK_SPACE )

import scene

scene.initSceneManager()
sceneMgr = scene.getSceneManager()
sceneMgr.defaultFont = annchienta.Font("assets/regular.ttf", 14)
sceneMgr.italicsFont = annchienta.Font("assets/italics.ttf", 14)

for i in range(9):
    sceneMgr.boxTextures.append( annchienta.Surface("assets/box"+str(i)+".png") )

import party

party.initPartyManager()
partyManager = party.getPartyManager()
partyManager.load("saves/new.xml")

import battle

battle.initBattleManager()
battleManager = battle.getBattleManager()
battleManager.loadEnemies("locations/common/enemies.xml")

mapMgr.run()
