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
options = ["Continue", "New Game", "Quit"]
background = annchienta.Surface("assets/title.png")
font = annchienta.Font("assets/italics.ttf", 24)
while inputManager.running():

    inputManager.update()

    videoManager.begin()
    videoManager.drawSurface( background, 0, 0 )

    for i in range(len(options)):
        if inputManager.hover( 0, 120+i*font.getLineHeight(), videoManager.getScreenWidth(), 120+(i+1)*font.getLineHeight() ):
            videoManager.setColor(0,0,0)

            if inputManager.buttonTicked(0):
                if options[i]=="Continue" or options[i]=="New Game":
                    partyManager.load("saves/save.xml" if options[i]=="Continue" else "saves/new.xml")
                    mapManager.run()
                    partyManager.free()
                if options[i]=="Quit":
                    inputManager.stop()

        else:
            videoManager.setColor(0,0,0,150)

        videoManager.drawStringCentered( font, options[i], 200, 120+i*font.getLineHeight() )

    videoManager.end()
