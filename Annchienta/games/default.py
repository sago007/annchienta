import annchienta
import time

device = annchienta.getDevice()
device.setVideoMode( 400, 300, False )

painter = annchienta.getPainter()
painter.reset()
surface = annchienta.Surface( "../img.png" )

start = time.time()
while start+10>time.time():
    surface.draw( 0, 0 )
    #painter.drawLine(10,10,390,290)
    painter.flip()
    time.sleep(0.01)
