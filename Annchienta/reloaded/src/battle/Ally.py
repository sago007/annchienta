import Combatant, SceneManager, Menu

class Ally( Combatant.Combatant ):

    def __init__( self, xmlElement ):
        
        # Base constructor
        Combatant.Combatant.__init__( self, xmlElement )
        
        # References
        self.sceneManager = SceneManager.getSceneManager()
        
        # Variables
        self.ally = True

        self.buildMenu()

    # Create a menu
    def buildMenu( self ):
    
        self.menu = Menu.Menu( self.name, "Select an action." )
        options = map( lambda q: Menu.MenuItem( q.name, q.description ), self.actions )
        self.menu.setOptions( options )
        self.menu.leftBottom()

    # Allies select an action from the menu
    def selectAction( self, battle ):
    
        menuItem = self.menu.pop( battle )
        if menuItem is None:
            return None
        found = filter( lambda a: a.name == menuItem.name, self.actions )
        return found[0]
        
    def drawInfo( self ):
    
        self.videoManager.pushMatrix()

        # Draw a quick black background
        self.videoManager.setColor( 0, 0, 0, 100 )
        self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), 20 )        
        
        # Draw the timer
        self.videoManager.pushMatrix()
        if self.timer>=100.0:
            self.videoManager.setColor( 161, 48, 0 )
        else:
            self.videoManager.setColor( 161, 120, 0 )
        self.videoManager.translate( self.videoManager.getScreenWidth()*0.4 + 3, 3 )
        width = int(0.01*self.timer*(self.videoManager.getScreenWidth()*0.6-6))
        self.videoManager.drawRectangle( 0, 0, width, 14 )
        self.videoManager.popMatrix()
        
        # Draw the combatant's name
        self.videoManager.setColor()
        self.videoManager.drawString( self.sceneManager.largeItalicsFont, self.name, self.sceneManager.margin, -3 )
        
        # Draw the combatant's hp
        self.videoManager.drawString( self.sceneManager.largeItalicsFont, str(self.healthStats["hp"])+"/"+str(self.healthStats["mhp"])+"HP", int(self.videoManager.getScreenWidth()*0.4)+self.sceneManager.margin, -3 )
        
        # Draw the combatant's mp
        self.videoManager.drawStringRight( self.sceneManager.largeItalicsFont, str(self.healthStats["mp"])+"MP", self.videoManager.getScreenWidth()-self.sceneManager.margin, -3 )
        
        self.videoManager.popMatrix()

