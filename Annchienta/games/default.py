import annchienta
import time

device = annchienta.Device()
device.setVideoMode( 400, 300, False )

painter = annchienta.Painter()
painter.setColor( 255, 0, 0 )
surface = annchienta.Surface( "../sunset.png" )

start = time.time()
while start+10>time.time():
    surface.draw( 0, 0 )
    painter.flip()
    time.sleep(0.01)
