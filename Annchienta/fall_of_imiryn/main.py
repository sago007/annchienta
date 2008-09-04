#!/usr/bin/python
import sys

# Add the source directory to the path so we can
# import modules from it.
sys.path.append("src")
sys.path.append("src/battle")

# This is only to be sure... the windows release
# might need it.
sys.path.append("lib")

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

import PartyManager
PartyManager.initPartyManager()
partyManager = PartyManager.getPartyManager()

import Menu

menu = Menu.Menu( "Main Menu", "I love my girlfriend." )
options = [ Menu.MenuItem("new", "Start a new game."),
            Menu.MenuItem("load", "Continue from the last save point."),
            Menu.MenuItem("quit", "Leave this great game.")
          ]
menu.setOptions( options )
menu.top()

videoManager.begin()
videoManager.end()
videoManager.end()

running = True
while running and inputManager.running():

    ans = menu.pop( None )

    if ans is not None:

        if ans.name == "quit":

            running = False

        else:

            loadFile = "save/new.xml"
            if ans.name == "load" and annchienta.isValidFile("save/save.xml"):
                loadFile = "save/save.xml"

            partyManager.load( loadFile )
            mapManager.run()
            partyManager.free()

annchienta.quit()
