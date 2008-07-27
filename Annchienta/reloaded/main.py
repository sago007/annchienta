#!/usr/bin/python
import sys

# Add the source directory to the path so we can
# import modules from it.
sys.path.append("src")

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
#mapManager.setOnUpdateScript("scripts/onupdate.py")

inputManager = annchienta.getInputManager()
inputManager.setInteractKey( annchienta.SDLK_SPACE )

import SceneManager
SceneManager.initSceneManager()
sceneManager = SceneManager.getSceneManager()
sceneManager.defaultFont = annchienta.Font("data/assets/regular.ttf", 14)
sceneManager.italicsFont = annchienta.Font("data/assets/italics.ttf", 14)
sceneManager.boxTextures = map( lambda i: annchienta.Surface("data/assets/box"+str(i)+".png"), range(9) )

# load a map
m = annchienta.Map( "data/locations/map.xml" )

# load the player
p = annchienta.Person( "aelaan", "data/locations/aelaan.xml" )
p.setInputControl()
p.setPosition( annchienta.Point( annchienta.TilePoint, 22, 10 ) )
m.addObject( p )

mapManager.cameraFollow( p )
mapManager.setCurrentMap( m )
mapManager.run()

m.removeObject( p )

annchienta.quit()

