import sys

# Add the scripts directory to the path so we can
# import modules from it.
sys.path.append("scripts")

import annchienta

videoManager = annchienta.getVideoManager()
videoManager.setVideoMode( 400, 300, "Annchienta", False )
videoManager.setClearColor(0,0,0)

mapManager = annchienta.getMapManager()
mapManager.setTileWidth(64)
mapManager.setTileHeight(32)
mapManager.setUpdatesPerSecond(60)
mapManager.setMaxAscentHeight(32)
mapManager.setMaxDescentHeight(32)
mapManager.setOnUpdateScript("scripts/onupdate.py")

inputManager = annchienta.getInputManager()
inputManager.setInteractKey( annchienta.SDLK_SPACE )

import scene

scene.initSceneManager()
sceneManager = scene.getSceneManager()
sceneManager.defaultFont = annchienta.Font("assets/regular.ttf", 14)
sceneManager.italicsFont = annchienta.Font("assets/italics.ttf", 14)
sceneManager.boxTextures = map( lambda i: annchienta.Surface("assets/box"+str(i)+".png"), range(9) )

import battle

battle.initBattleManager()
battleManager = battle.getBattleManager()
battleManager.loadEnemies("locations/common/enemies.xml")

import party

# Depends on battleManager
party.initPartyManager()
partyManager = party.getPartyManager()

while inputManager.running():

    a = sceneManager.chat(None, "What do you want to do?", ["Start a new game.", "Load a previously saved game."])
    partyManager.load("saves/save.xml" if a else "saves/new.xml")

    mapManager.run()
    partyManager.free()
