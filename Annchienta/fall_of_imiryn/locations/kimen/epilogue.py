import annchienta, SceneManager

# Get references...
engine = annchienta.getEngine()
videoManager = annchienta.getVideoManager()
sceneManager = SceneManager.getSceneManager()

# A simple class that displays the ship
# over a scrolling background.
class FlyAnimation:

    def __init__( self ):

        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
       
        self.background = annchienta.Surface( "images/backgrounds/land.png" )
        self.ship = annchienta.Surface( "sprites/ship_small.png" )

        self.backgroundY = 0.0
        self.lastUpdate = None

    def update( self, updateInputToo ):

        ticks = self.engine.getTicks()
        ms = ticks - self.lastUpdate if self.lastUpdate else 0
        self.backgroundY += 0.1*float(ms)
        self.backgroundY %= self.videoManager.getScreenHeight()
        self.lastUpdate = ticks

    def draw( self ):

        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY) )
        self.videoManager.drawSurface( self.background, 0, int(self.backgroundY-self.videoManager.getScreenHeight()) )

        self.videoManager.drawSurface( self.ship, (self.videoManager.getScreenWidth()-self.ship.getWidth())/2,
                                                  (self.videoManager.getScreenHeight()-self.ship.getHeight())/2 )

# Create an object like this.
flyAnimation = FlyAnimation()

# Now display some text with this animation
sceneManager.text( "August:\nAnd so we returned to the Imiryn Empirial City.", flyAnimation, True )
sceneManager.text( "August:\nWe were quite excited, but scared, too.", flyAnimation, True )
sceneManager.text( "August:\nWhat if we were arrested and executed? After all, some people had very good reasons to hate us now.", flyAnimation, True )
sceneManager.text( "August:\nMarch was sure we were going to be punished by the Empire himself.", flyAnimation, True )
sceneManager.text( "August:\nAvril thought we would get a fair trial, and that the judge would have no choice but choosing our side.", flyAnimation, True )
sceneManager.text( "August:\nTo tell you the truth, I didn't really care. I had done what I had to do.", flyAnimation, True )
sceneManager.text( "August:\nSo much had happened... it felt like we had gotten ten years older in, what would it be, two weeks?", flyAnimation, True )
sceneManager.text( "August:\nAvril was talking about the future of the Laustwan as we approached the Imiryn Empirial City...", flyAnimation, True )

# Animation done... display text with the background of a ruined empirial city.
imirynBurns = annchienta.Surface( "images/storyline/imiryn_burns.png" )
videoManager.clear()
videoManager.drawSurface( imirynBurns, 0, 0 )
videoManager.flip()
videoManager.flip()

sceneManager.text( "August:\nNot quite the scene we expected.", None, True )
sceneManager.text( "August:\nThe pirates had attacked the city... and won.", None, True )
sceneManager.text( "August:\nThere was nothing left to return to. Together with the few survivors, we had to leave the location.", None, True )
sceneManager.text( "August:\nMost Laustwan had fled by then.", None, True )
sceneManager.text( "August:\nI still did not care.", None, True )
sceneManager.text( "It would take hundreds of year before the descendants of the survivors regained some power.", None, True )
sceneManager.text( "Because of what had happened in the past, they did not want to hear the name Imiryn Empire. By that time, everyone knew the Legend of the Laustwan.", None, True )
sceneManager.text( "They called themselves The Dark Lion Alliance, referring to something one of their first leaders called Avril once said:", None, True )
sceneManager.text( "Like a dark lion, engulfed in shadow, watching a sparkle of light. Just like that, we all can see some hope.", None, True )
sceneManager.text( "And hope was born again.", None, True )

sceneManager.fade()
sceneManager.text( "The End. I sincerely hope you enjoyed this game. You can always tell me what you think at jaspervdj@gmail.com. Your most humble and obedient servant, Jasper.", None, True )

mapManager.stop()
