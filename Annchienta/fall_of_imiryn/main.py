#!/usr/bin/python
import sys

# Add the source directory to the path so we can
# import modules from it.
sys.path.append("src")

# This is only to be sure... the windows release
# might need it.
sys.path.append("lib")

import annchienta

# Fire up the engine.
annchienta.init("save")

engine = annchienta.getEngine()

# Init VideoManager.
videoManager = annchienta.getVideoManager()
videoManager.setVideoMode( 400, 300, "Annchienta", False )
videoManager.setClearColor(0,0,0)

# Init AudioManager.
audioManager = annchienta.getAudioManager()
audioManager.playMusic("music/title.ogg")

# Init MapManager.
mapManager = annchienta.getMapManager()
mapManager.setTileWidth(64)
mapManager.setTileHeight(32)
mapManager.setUpdatesPerSecond(60)
mapManager.setMaxAscentHeight(32)
mapManager.setMaxDescentHeight(32)
mapManager.setOnUpdateScript("src/onUpdate.py")

# Init InputManager.
inputManager = annchienta.getInputManager()
inputManager.setInteractKey( annchienta.SDLK_SPACE )

# Init SceneManager.
import SceneManager
SceneManager.initSceneManager()
sceneManager = SceneManager.getSceneManager()
sceneManager.defaultFont = annchienta.Font("assets/regular.ttf", 14)
sceneManager.italicsFont = annchienta.Font("assets/italics.ttf", 14)
sceneManager.largeRegularFont = annchienta.Font("assets/regular.ttf", 20)
sceneManager.largeItalicsFont = annchienta.Font("assets/italics.ttf", 20)
sceneManager.boxTextures = map( lambda i: annchienta.Surface("assets/box"+str(i)+".png"), range(9) )

# Init PartyManager.
import PartyManager
PartyManager.initPartyManager()
partyManager = PartyManager.getPartyManager()

# Init BattleManager.
import BattleManager
BattleManager.initBattleManager()

# Start Main menu.
import Menu

# Load a title background.
splashImage = annchienta.Surface( "images/backgrounds/splash.png" )
videoManager.begin()
videoManager.drawSurface( splashImage, 0, 0 )
videoManager.end()
videoManager.end()
engine.delay(2000)
sceneManager.fade( 255, 255, 255, 2000 )

titleBackground = annchienta.Surface( "images/backgrounds/title.png" )

running = True
while running and inputManager.running():

    videoManager.begin()
    videoManager.drawSurface( titleBackground, 0, 0 )
    videoManager.end()
    videoManager.end()

    menu = Menu.Menu( "Main Menu", "I love my girlfriend." )
    options = [ Menu.MenuItem("new", "Start a new game."),
                Menu.MenuItem("load", "Continue from the last save point."),
                Menu.MenuItem("fullscreen", "Enable or disable fullscreen mode."),
                Menu.MenuItem("quit", "Leave this great game.")
              ]
    menu.setOptions( options )
    menu.top()
    ans = menu.pop( None )

    if ans is not None:

        if ans.name == "quit":

            running = False

        elif ans.name == "fullscreen":

            videoManager.setVideoMode( videoManager.getScreenWidth(), videoManager.getScreenHeight(), "Annchienta", not videoManager.isFullScreen() )

        else:

            loadFile = "save/new.xml"
            if ans.name == "load" and engine.isValidFile("save/save.xml"):
                loadFile = "save/save.xml"

            partyManager.load( loadFile )
            mapManager.run()
            partyManager.free()

annchienta.quit()

