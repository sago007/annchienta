#!/usr/bin/python
import sys

# Add the source directory to the path so we can
# import modules from it.
sys.path.append("src")
sys.path.append("src/battle")

# This is only to be sure... the windows release
# might need it.
sys.path.append("../lib")

import annchienta

# Fire up the engine.
annchienta.init("save")

engine = annchienta.getEngine()

videoManager = annchienta.getVideoManager()
videoManager.setVideoMode( 400, 300, "Annchienta", False )
videoManager.setClearColor(0,0,0)

mapManager = annchienta.getMapManager()
mapManager.setTileWidth(64)
mapManager.setTileHeight(32)
mapManager.setUpdatesPerSecond(60)
mapManager.setMaxAscentHeight(32)
mapManager.setMaxDescentHeight(32)
mapManager.setOnUpdateScript("src/OnUpdate.py")

inputManager = annchienta.getInputManager()
inputManager.setInteractKey( annchienta.SDLK_SPACE )

import SceneManager
SceneManager.initSceneManager()
sceneManager = SceneManager.getSceneManager()
sceneManager.defaultFont = annchienta.Font("assets/regular.ttf", 14)
sceneManager.italicsFont = annchienta.Font("assets/italics.ttf", 14)
sceneManager.largeRegularFont = annchienta.Font("assets/regular.ttf", 20)
sceneManager.largeItalicsFont = annchienta.Font("assets/italics.ttf", 20)
sceneManager.boxTextures = map( lambda i: annchienta.Surface("assets/box"+str(i)+".png"), range(9) )

loadFile = "save/new.xml"
if "--load" in sys.argv:
    loadFile = "save/save.xml"

import PartyManager
PartyManager.initPartyManager()
partyManager = PartyManager.getPartyManager()
partyManager.load( loadFile )

mapManager.run()

partyManager.free()

annchienta.quit()

