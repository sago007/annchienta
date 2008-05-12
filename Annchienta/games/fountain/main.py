import annchienta
import particle

engine = annchienta.getEngine()

videoManager = annchienta.getVideoManager()
videoManager.setVideoMode( 640, 480, "Fountain!" )
videoManager.setClearColor( 0, 0, 0 )

inputManager = annchienta.getInputManager()

emitter = particle.Emitter()

while inputManager.running():

    start = engine.getTicks()

    inputManager.update()
    emitter.update()

    videoManager.begin()
    emitter.draw()
    videoManager.end()

    delay = 20+start-engine.getTicks()
    if delay>0:
        engine.delay( delay )

