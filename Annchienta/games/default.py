import annchienta

device = annchienta.getDevice()
device.setVideoMode( 400, 300, "Annchienta", False )

painter = annchienta.getPainter()
painter.reset()

inputManager = annchienta.getInputManager()

surface = annchienta.Surface( "../testdata/img.png" )

font = annchienta.Font( "../testdata/font.ttf", 50 )

while inputManager.running():
    
    inputManager.update()
    
    painter.setColor()
    surface.draw( 0, 0 )
    painter.setColor(255,255,0,30)
    
    if inputManager.keyDown( annchienta.SDLK_a ):
        font.draw(10,10,"Hello world!")
    
    painter.flip()
