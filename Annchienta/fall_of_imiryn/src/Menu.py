import annchienta, SceneManager

class MenuItem:

    # Constructs and sets stuff like name and tooltip
    def __init__( self, name, toolTip=None ):
    
        self.name, self.toolTip = name, toolTip
        
        # It's not a menu, it's purely a menu item
        self.isMenu = False

## \brief A simple Menu.
#
#  Uses video buffer 6.
class Menu(MenuItem):

    def __init__( self, name, toolTip=None ):
    
        # Base constructor
        MenuItem.__init__( self, name, toolTip )
        
        # Get references
        self.inputManager = annchienta.getInputManager()
        self.videoManager = annchienta.getVideoManager()
        self.mapManager = annchienta.getMapManager()
        self.sceneManager = SceneManager.getSceneManager()
        
        # This is a menu, not just a menu item.
        self.isMenu = True

        # Size of the menu
        self.width, self.height = 0, 0

        # Position on the screen
        self.x, self.y = 0, 0

        # If the tooltip should be drawn on top of the screen
        self.toolTipOnTop = True

        # Kinda self explanatory
        self.maxItemsInColumn = 4

        # The options in the menu. Use setOptions() to set them!
        self.options = []

    def setOptions( self, options=None ):

        # Set the options only if provided
        if not options is None:
            self.options = options

        # Calculate number of rows and columns
        self.rows = len(self.options) if len(self.options)<self.maxItemsInColumn else self.maxItemsInColumn
        self.columns = (len(self.options)/self.maxItemsInColumn)
        if len(self.options)%self.maxItemsInColumn:
            self.columns += 1

        if self.columns <= 1:
            self.columns = 1

        # Find the longest name in pixels to base the width on
        names = map( lambda o: o.name, self.options ) + [self.name]
        self.longest = max( map( lambda n: self.sceneManager.defaultFont.getStringWidth(n.capitalize()), names ) )
        
        # Use this to calculate the menu width, then calculate menu height
        self.width = self.sceneManager.margin + (self.longest + self.sceneManager.margin)*self.columns
        self.height = self.rows*self.sceneManager.defaultFont.getLineHeight() + self.sceneManager.italicsFont.getLineHeight() + 2*self.sceneManager.margin

        # Work recursive for submenus
        for m in self.options:
            if m.isMenu:
                m.setOptions()

    # Sets the menu on top of the screen
    def top( self ):
        self.toolTipOnTop = False
        self.y = self.sceneManager.margin
        self.x = (self.videoManager.getScreenWidth()-self.width)/2
        # Work recursive for submenus
        for m in self.options:
            if m.isMenu:
                m.top()

    # Sets the menu on top of the screen, on the right side...
    def topRight( self ):
        self.toolTipOnTop = False
        self.y = self.sceneManager.margin
        self.x = self.videoManager.getScreenWidth()-self.width-self.sceneManager.margin
        # Work recursive for submenus
        for m in self.options:
            if m.isMenu:
                m.topRight()

    # Sets the menu in the left bottom of the screen
    def leftBottom( self ):
        self.toolTipOnTop = True
        self.y = self.videoManager.getScreenHeight()-self.height-self.sceneManager.margin#*4-self.sceneManager.defaultFont.getLineHeight()
        self.x = self.sceneManager.margin
        # Work recursive for submenus
        for m in self.options:
            if m.isMenu:
                m.leftBottom()

    ## Pops the menu
    #
    #  \param backgroundProcess The process handling the background. This object should have update( updateInputToo ) and draw() methods. This is usually the MapManager instance. If set to None, the initial background is kept.
    #  \return The chosen menu option, or None if canceled.
    def pop( self, backgroundProcess = annchienta.getMapManager() ):

        self.backgroundProcess = backgroundProcess

        # Disable character input/movement
        originalInputMode = self.inputManager.getInputMode()
        self.inputManager.setInputMode( annchienta.CinematicMode )

        # Player stops walking...
        inputControlledPerson = self.inputManager.getInputControlledPerson()
        if inputControlledPerson:
            inputControlledPerson.setStandAnimation()

        # Store background if we don't have a process to generate it
        if not backgroundProcess:
            self.videoManager.storeBuffer(6)

        # Avoid accidental clicks
        self.inputManager.update()
        
        # Initialize some stuff
        self.done = False
        self.clickedItem = None

        while not self.done and self.clickedItem is None:
        
            self.videoManager.clear()
            
            # Draw appropriate background
            if backgroundProcess:
                backgroundProcess.draw()
            else:
                self.videoManager.restoreBuffer(6)
            
            # Draw self
            self.render()
            
            self.videoManager.flip()

            self.update()

        self.mapManager.resync()

        self.videoManager.setColor()
        
        if not backgroundProcess:
            self.videoManager.restoreBuffer(6)

        # Restore input mode
        self.inputManager.setInputMode( originalInputMode )

        # If canceled, return None
        if self.clickedItem is None:
            return None
        else:
            # If the chosen item is a submenu, recursively call that submenu.
            if self.clickedItem.isMenu:
                sub = self.clickedItem.pop( backgroundProcess )
                # If the submenu was canceled, we return to this menu
                if sub is None:
                    return self.pop( backgroundProcess )
                # Return the item chosen by the submenu
                else:
                    return sub
            # Simply return the item.
            else:
                return self.clickedItem

    def update( self ):

        # Update everything
        self.inputManager.update()
        if self.backgroundProcess:
            self.backgroundProcess.update(False)

        # Check for actions
        if self.inputManager.buttonTicked( 1 ):
            self.done = True

        if not self.inputManager.running():
            self.done = True

    def render( self ):

        hover = None

        # Draw box for the menu
        self.sceneManager.drawBox( self.x, self.y, self.x+self.width, self.y+self.height )
        self.videoManager.pushMatrix()

        # Draw title
        self.videoManager.translate( self.x, self.y )
        self.videoManager.drawStringCentered( self.sceneManager.italicsFont, self.name.capitalize(), self.width/2, self.sceneManager.margin )

        # Move to the start of the items
        self.videoManager.translate( self.sceneManager.margin, self.sceneManager.margin+ self.sceneManager.italicsFont.getLineHeight() )

        sx, sy = self.x+self.sceneManager.margin, self.y+self.sceneManager.margin+ self.sceneManager.italicsFont.getLineHeight()

        # Render all items
        for x in range(self.columns):
            for y in range(self.rows):
                idx = x*self.rows+y
                if idx<len(self.options):
                    o = self.options[ idx ]
                    if self.inputManager.hover( sx+x*(self.longest+self.sceneManager.margin), sy+y*self.sceneManager.defaultFont.getLineHeight(), sx+(x+1)*(self.longest+self.sceneManager.margin), sy+(y+1)*self.sceneManager.defaultFont.getLineHeight() ):
                        self.sceneManager.activeColor()
                        hover = o
                        if self.inputManager.buttonTicked(0):
                            self.clickedItem = o
                    else:
                        self.sceneManager.inactiveColor()
                    self.videoManager.drawString( self.sceneManager.defaultFont, o.name.capitalize(), x*(self.longest+self.sceneManager.margin), y*self.sceneManager.defaultFont.getLineHeight() )

        self.videoManager.popMatrix()

        self.sceneManager.defaultColor()

        # Render tooltip
        if hover is not None:
            if hover.toolTip is not None:
                self.videoManager.pushMatrix()

                # Count the lines we have to draw
                lines = hover.toolTip.split('\n')

                # Calculate tooltip height
                h = self.sceneManager.margin*2+self.sceneManager.defaultFont.getLineHeight()*len(lines)

                # Calculate tooltip y
                y = self.sceneManager.margin if self.toolTipOnTop else self.videoManager.getScreenHeight()-self.sceneManager.margin-h

                # Draw the tooltip
                self.sceneManager.drawBox( self.sceneManager.margin, y, self.videoManager.getScreenWidth()-self.sceneManager.margin, y+h )
                self.videoManager.translate( 0, y+self.sceneManager.margin )

                for line in lines:
                    self.videoManager.drawString( self.sceneManager.defaultFont, str(line), self.sceneManager.margin*2, 0 )
                    self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )

                self.videoManager.popMatrix()

