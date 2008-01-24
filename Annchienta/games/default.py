from annchienta import *

video = getVideoManager()
video.setVideoMode( 400, 300, "Annchienta", False )

inputManager = getInputManager()

surface = Surface( "../testdata/img2.png" )

video.drawSurface( surface, 0, 0 )

font = Font( "../testdata/font.ttf", 50 )

part = video.grabBuffer( 50, 25, 75, 50 )

while inputManager.running():
    
    inputManager.update()
    
    video.drawSurface( part, 0, 0 )
    
    video.drawText( font, "Hello", 400 - font.getStringWidth("Hello"), 0 )
    
    video.flip()
    