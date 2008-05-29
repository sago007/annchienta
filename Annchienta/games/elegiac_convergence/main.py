import sys

# Add the scripts directory to the path so we can
# import modules from it.
sys.path.append("scripts")

import annchienta

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
mapManager.setOnUpdateScript("scripts/onupdate.py")

inputManager = annchienta.getInputManager()
inputManager.setInteractKey( annchienta.SDLK_SPACE )

audioManager = annchienta.getAudioManager()
audioManager.playMusic("music/title.ogg")

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

# Main menu
title_background = annchienta.Surface("assets/title.png")
title_font = annchienta.Font("assets/italics.ttf", 24)
surf = annchienta.Surface( 400, 300, 3 )
while inputManager.running():

    inputManager.update()

    videoManager.begin()
    videoManager.drawSurface( title_background, 0, 0 )

    options = ["Continue", "New Game", "Quit"]
    for i in range(len(options)):
        if inputManager.hover( 0, 120+i*title_font.getLineHeight(), videoManager.getScreenWidth(), 120+(i+1)*title_font.getLineHeight() ):
            videoManager.setColor(0,0,0)

            if inputManager.buttonTicked(0):
                if options[i]=="Continue" or options[i]=="New Game":

                    # Choose appropriate filename.
                    filename = "saves/save.xml" if options[i]=="Continue" else "saves/new.xml"
                    # Fallback
                    if not annchienta.isValidFile( filename ):
                        filename = "saves/new.xml"

                    partyManager.load( filename )
                    mapManager.run()
                    partyManager.free()
                    inputManager.update()
                elif options[i]=="Quit":
                    inputManager.stop()

        else:
            videoManager.setColor(0,0,0,150)

        if inputManager.running():
            videoManager.drawStringCentered( title_font, str(options[i]), 200, 120+i*title_font.getLineHeight() )

    #videoManager.boxBlur( 100, 100, 300, 200, 6 )
    #videoManager.grabBuffer( surf )
    #videoManager.begin()
    #videoManager.drawSurface( surf, 0, 0, 0, 0, 200, 100 )
    videoManager.end()
