#!/usr/bin/python
import sys
import os

# Add the source directory to the path so we can
# import modules from it.
sys.path.append("src")

# This is only to be sure... the windows release
# might need it.
sys.path.append("lib")

import annchienta

try:
    os.mkdir(os.path.join(os.path.expanduser("~"), ".fall-of-imiryn"))
except:
    pass

# Fire up the engine.
annchienta.init(os.path.join(os.path.expanduser("~"), ".fall-of-imiryn"))

engine = annchienta.getEngine()

# Init VideoManager.
videoManager = annchienta.getVideoManager()
videoManager.setVideoMode( 400, 300, "Annchienta", False, 1 )
videoManager.setClearColor(0,0,0)

# Init AudioManager.
audioManager = annchienta.getAudioManager()
audioManager.setVolume( 0.33 )
audioManager.playMusic("music/title_1a.ogg")

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
SceneManager.init()
sceneManager = SceneManager.getSceneManager()

# Init PartyManager.
import PartyManager
PartyManager.init()
partyManager = PartyManager.getPartyManager()

# Init BattleManager.
import BattleManager
BattleManager.init()

# Start Main menu.
import Menu
import MenuItem

# Display a splash image. removed for quicker testing purposes
#splashImage = annchienta.Surface( "images/backgrounds/splash.png" )
start = engine.getTicks()
#while engine.getTicks() < start + 1000:
#    videoManager.clear()
#    videoManager.drawSurface( splashImage, 0, 0 )
#    videoManager.flip()
#sceneManager.fade( 255, 255, 255, 2000 )

# Load a title background.
titleBackground = annchienta.Surface( "images/storyline/title.png" )

running = True
while running and inputManager.isRunning():

    videoManager.clear()
    videoManager.drawSurface( titleBackground, 0, 0 )
    videoManager.flip()
    videoManager.flip()

    menu = Menu.Menu( "Main Menu", "I love my girlfriend." )
    options = [ MenuItem.MenuItem("new", "Start a new game."),
                MenuItem.MenuItem("load", "Continue from the last save point."),
                MenuItem.MenuItem("video size", "Change the video size. (Experimental)\n(A larger size might slow down or crash the game.)"),
                MenuItem.MenuItem("quit", "Leave this great game.")
              ]
    menu.setOptions( options )
    menu.leftBottom()
    menuItem = menu.pop( None )

    if menuItem is not None:

        if menuItem.getName() == "quit":

            running = False

        elif menuItem.getName() == "video size":

            scale = 2 if videoManager.getVideoScale()==1 else 1
            videoManager.setVideoMode( videoManager.getScreenWidth(), videoManager.getScreenHeight(), "Annchienta", videoManager.isFullScreen(), scale )

        else:

            loadFile = "save/new.xml"
            previouslySavedFile = os.path.join(os.path.expanduser("~"), ".fall-of-imiryn/save.xml")
            if menuItem.getName() == "load" and engine.isValidFile(previouslySavedFile):
                loadFile = previouslySavedFile

            partyManager.load( loadFile )
            mapManager.run()
            partyManager.free()

annchienta.quit()
