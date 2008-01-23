import annchienta
import time

device = annchienta.getDevice()
device.setVideoMode( 400, 300, False )

painter = annchienta.getPainter()
painter.reset()

surface = annchienta.Surface( "../testdata/img.png" )

font = annchienta.Font( "../testdata/font.ttf", 50 )

start = time.time()

rotation = 0

while start+10>time.time():
    
    painter.setColor()
    surface.draw( 0, 0 )
    painter.pushMatrix()
    painter.translate( 200, 150 )
    painter.rotate( rotation )
    painter.scale( 100, 100 )
    painter.drawTriangle( -1, 1, 0, -1, 1, 1 )
    painter.popMatrix()
    painter.setColor(255,255,0,30)
    font.draw(10,10,"Hello world!")
    
    rotation += 1
    
    painter.flip()
    time.sleep(0.01)
