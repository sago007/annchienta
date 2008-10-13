import annchienta, Game

class Menu:

    def __init__( self ):
    
        # Get nessecary references
        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.audioManager = annchienta.getAudioManager()
        self.cacheManager = annchienta.getCacheManager()
        
        # Set video mode.
        self.videoManager.setVideoMode( 480, 320, "Happy Squirrel Land!" )
        self.inputManager.setMouseVisibility( False )
        
        self.game = Game.Game()
        
    def run( self ):

        self.audioManager.playMusic("data/happy_music.ogg")
        self.intro()
        while self.inputManager.running():
            self.audioManager.playMusic("data/hard_music.ogg")
            self.game.run()
            self.audioManager.playMusic("data/happy_music.ogg")
            self.gameOver()        

    def intro( self ):
    
        strings = ["Allow me to tell you a story... (click to continue)",
                   "It's about Happy Squirrel Land.",
                   "This place lies very deep in unexplored forests.",
                   "It is inhabited by many happy squirrels.",
                   "They dance, talk and have fun all day long.",
                   "Enjoying the beauty of nature, everyone is happy there.",
                   "But well... there is one exception.",
                   "An unhappy squirrel arrived from nearby forests a few days ago.",
                   "He was not at all like the other squirrels.",
                   "He talked about sad things and listened to death metal.",
                   "That's when the other squirrels decided to make him happy.",
                   "They would talk to him about love and friendship.",
                   "They would tell him about the beautiful things in the world.",
                   "The unhappy squirrel, however, could not appreciate this.",
                   "Use the arrow keys to move, and your mouse to shoot.",
                   "Kill the happy squirrels before they infect you with happiness." ]
                   
                   
        for s in strings:
            self.text( s )
        
    def gameOver( self ):
    
        self.text( "Too bad, they made you happy. You killed "+str(self.game.bodycount)+" of 'em." )
        
    def text( self, string ):
    
        self.videoManager.begin()
        self.videoManager.drawSurface( self.game.background, 0, 0 )
        self.videoManager.setColor( 0, 0, 0, 100 )
        self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), 50 )
        self.videoManager.setColor()
        self.videoManager.drawString( self.game.font, string, 10, 16 )
        self.videoManager.setColor( 255, 255, 255, 100 )
        self.videoManager.drawStringRight( self.game.font, "Graphics and programming by Jasper Van der Jeugt", self.videoManager.getScreenWidth()-10, self.videoManager.getScreenHeight()-20 )
        self.videoManager.end()
        self.waitForClick()
        
    def waitForClick( self ):

        self.videoManager.end()
        self.videoManager.storeBuffer(7)
        self.inputManager.update()
        while self.inputManager.running() and not self.inputManager.buttonTicked(0):
            self.inputManager.update()
            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.videoManager.end()

