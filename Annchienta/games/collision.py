import annchienta
import time

videoMgr = annchienta.getVideoManager()
audioMgr = annchienta.getAudioManager()
inputMgr = annchienta.getInputManager()

videoMgr.setVideoMode( 400, 300, "Annchienta", False )

surface = annchienta.Surface("maps/aelaan.png")
mask = annchienta.Mask("maps/mask.png")

x1 = y1 = 0
x2 = y2 = 200

while inputMgr.running():

    videoMgr.drawSurface( surface, x1, y1, 0, 0, 64, 90 )
    videoMgr.drawSurface( surface, x2, y2, 0, 0, 64, 90 )

    if mask.collision( x1, y1, mask, x2, y2 ):
        videoMgr.setColor(255,0,0,100)
        videoMgr.drawRectangle(0,0,400,300)
        videoMgr.setColor()

    videoMgr.flip()

    inputMgr.update()

    if inputMgr.keyDown( annchienta.SDLK_LEFT ):
        x1 -= 1
    if inputMgr.keyDown( annchienta.SDLK_RIGHT ):
        x1 += 1
    if inputMgr.keyDown( annchienta.SDLK_DOWN ):
        y1 += 1
    if inputMgr.keyDown( annchienta.SDLK_UP ):
        y1 -= 1

    time.sleep( 0.01 )
