import math
import annchienta

class Particle:

    def __init__( self ):
        self.videoManager = annchienta.getVideoManager()

    def update( self ):

        # update life
        self.life += 1

        # gravity
        self.vy += .02

        # update position
        self.x += self.vx
        self.y += self.vy

    def draw( self ):

        self.videoManager.setColor( 255, 255, 255, int(255.0*(1.0-float(self.life)/float(self.maxlife))) )

        self.videoManager.pushMatrix()
        self.videoManager.translate( self.x, self.y )
        self.videoManager.translate( -self.surface.getWidth()/2, -self.surface.getHeight()/2 )
        self.videoManager.drawSurface( self.surface, 0, 0 )
        self.videoManager.popMatrix()

class Emitter:

    def __init__( self ):

        self.inputManager = annchienta.getInputManager()
        self.videoManager = annchienta.getVideoManager()

        self.x = self.videoManager.getScreenWidth()/2
        self.y = self.videoManager.getScreenHeight()/2

        self.particles = []

        self.surface = annchienta.Surface("particle.png")

    def update( self ):

        if annchienta.randFloat()<0.3:
            p = Particle()
            p.surface = self.surface
            p.x, p.y = self.x, self.y
            p.vx, p.vy = 2, -2
            p.life, p.maxlife = 0, annchienta.randInt(60,200)

            rx, ry = float(self.inputManager.getMouseX()-self.x), float(self.inputManager.getMouseY()-self.y)
            d = 1/annchienta.distance( 0, 0, rx, ry )
            rx *= d
            ry *= d

            p.vx, p.vy = 2.0*rx, 2.0*ry

            self.particles += [p]

        for p in self.particles:
            p.update()

        # remove dead ones
        self.particles = filter( lambda p: p.life <= p.maxlife, self.particles )

    def draw( self ):
        
        for p in self.particles:
            p.draw()
