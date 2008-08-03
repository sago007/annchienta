import Combatant, Menu

class Ally( Combatant.Combatant ):

    def __init__( self, xmlElement ):
        
        # Base constructor
        Combatant.Combatant.__init__( self, xmlElement )
        
        # Variables
        self.ally = True

        self.buildMenu()

    # Create a menu
    def buildMenu( self ):
    
        self.menu = Menu.Menu( self.name, "Select an action." )
        subs = []
        for action in self.actions:
            added = False
            for sub in subs:
                if sub.name == action.category:
                    sub.options += [Menu.MenuItem( action.name, action.description+" ("+str(action.cost)+"MP)" )]
                    added = True
            if not added:
                if action.category=="top":
                    subs += [Menu.MenuItem( action.name, action.description+" ("+str(action.cost)+"MP)" )]
                else:
                    newsub = Menu.Menu( action.category )
                    newsub.options += [Menu.MenuItem( action.name, action.description+" ("+str(action.cost)+"MP)" )]
                    subs += [newsub]
                
        # set options and align
        self.menu.setOptions( subs )
        self.menu.leftBottom()

    # Allies select an action from the menu. returns (action, target)
    def selectAction( self, battle ):
    
        menuItem = self.menu.pop( battle )
        if menuItem is None:
            return None, None
        found = filter( lambda a: a.name == menuItem.name, self.actions )

        action = found[0]

        # Check if there is enough mp
        if self.healthStats["mp"] < action.cost:
            battle.lines += [combatant.name.capitalize()+" doesn't have enough MP!"]
            return None, None
            
        # Select a target when needed
        target = None
        if action.target:
            target = self.selectTarget( battle )
            if target is None:
                return None, None

        return action, target
        
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

    def selectTarget( self, battle ):
    
        done = False
        target = None
        while not done:
            
            # Update
            battle.update( False )
            
            # Update input
            battle.inputManager.update()
            
            target = None
            
            # Find out hover target
            for c in battle.combatants:
                if battle.inputManager.hover( int(c.position.x-c.width/2), int(c.position.y-c.height/2), int(c.position.x+c.width/2), int(c.position.y+c.height/2) ):
                    target = c
                    c.hover = True
            
            # Check for input
            if not battle.inputManager.running() or battle.inputManager.buttonTicked(1):
                target = None
                done = True
            if battle.inputManager.buttonTicked(0):
                done = True
            
            # Draw
            battle.videoManager.begin()
            battle.draw()
            
            # Draw "select target"
            self.sceneManager.activeColor()
            self.videoManager.drawString( self.sceneManager.largeItalicsFont, "Select Target", self.sceneManager.margin, self.videoManager.getScreenHeight()-20*(len(battle.allies)+1) )
            
            battle.videoManager.end()

            # Reset hover
            for c in battle.combatants:
                c.hover = False

        return target

