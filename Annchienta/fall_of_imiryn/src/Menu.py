import MenuItem
import annchienta, SceneManager

## \brief A simple Menu.
#
#  Uses video buffer 6.
class Menu( MenuItem.MenuItem ):

    def __init__( self, name, toolTip=None ):
    
        # Base constructor
        MenuItem.MenuItem.__init__( self, name, toolTip )
        
        # Get references
        self.inputManager = annchienta.getInputManager()
        self.videoManager = annchienta.getVideoManager()
        self.mapManager = annchienta.getMapManager()
        self.sceneManager = SceneManager.getSceneManager()

        # Flags
        self.done = False
        self.canceled = False
        
        # Size of the menu
        self.width, self.height = 0, 0

        # Position on the screen
        self.x, self.y = 0, 0
        self.columns = 1
        self.rows = 1

        # If the tooltip should be drawn on top of the screen
        self.toolTipOnTop = True

        # Kinda self explanatory
        self.maxItemsInColumn = 4

        # The options in the menu. Use setOptions() to set them!
        self.options = []

        # The currently selected item index
        self.selectedOptionIndex = 0
        self.selectedOption = None

    def isMenu( self ):
        return True

    def getOptionIndex( self, item ):
        for i in range( len(self.options) ):
            if self.options[i] is item:
                return i
        return 0

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
        names = [ o.getName() for o in self.options ] + [self.name]
        self.longest = max( [ self.sceneManager.getDefaultFont().getStringWidth(n.capitalize()) for n in names ] )
        
        # Use this to calculate the menu width, then calculate menu height
        self.width = self.sceneManager.getMargin() + (self.longest + self.sceneManager.getMargin())*self.columns
        self.height = self.rows*self.sceneManager.getDefaultFont().getLineHeight() + self.sceneManager.getItalicsFont().getLineHeight() + 2*self.sceneManager.getMargin()

        # Work recursive for submenus
        for m in self.options:
            if m.isMenu():
                m.setOptions()

    # Sets the menu on top of the screen
    def top( self ):
        self.toolTipOnTop = False
        self.y = self.sceneManager.getMargin()
        self.x = int( (self.videoManager.getScreenWidth()-self.width)/2 )
        # Work recursive for submenus
        for m in self.options:
            if m.isMenu():
                m.top()

    # Sets the menu on top of the screen, on the right side...
    def topRight( self ):
        self.toolTipOnTop = False
        self.y = self.sceneManager.getMargin()
        self.x = self.videoManager.getScreenWidth()-self.width-self.sceneManager.getMargin()
        # Work recursive for submenus
        for m in self.options:
            if m.isMenu():
                m.topRight()

    # Sets the menu on top of the screen, on the left side...
    def topLeft( self ):
        self.toolTipOnTop = False
        self.y = self.sceneManager.getMargin()
        self.x = self.sceneManager.getMargin()
        # Work recursive for submenus
        for m in self.options:
            if m.isMenu():
                m.topLeft()
                
    # Sets the menu in the left bottom of the screen
    def leftBottom( self ):
        self.toolTipOnTop = True
        self.y = self.videoManager.getScreenHeight()-self.height-self.sceneManager.getMargin()#*4-self.sceneManager.getDefaultFont().getLineHeight()
        self.x = self.sceneManager.getMargin()
        # Work recursive for submenus
        for m in self.options:
            if m.isMenu():
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
        self.selectedOption = None
        self.selectedOptionIndex = 0

        while not self.done:
        
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
        if self.canceled:
            return None
        else:
            # If the chosen item is a submenu, recursively call that submenu.
            if self.selectedOption.isMenu():
                sub = self.selectedOption.pop( backgroundProcess )
                # If the submenu was canceled, we return to this menu
                if sub is None:
                    return self.pop( backgroundProcess )
                # Return the item chosen by the submenu
                else:
                    return sub
            # Simply return the item.
            else:
                return self.selectedOption

    def update( self ):

        # Update everything
        self.inputManager.update()
        if self.backgroundProcess:
            self.backgroundProcess.update(False)

        # Check for actions
        if self.inputManager.buttonTicked( 1 ) or self.inputManager.cancelKeyTicked():
            self.done = True
            self.canceled = True

        if self.inputManager.buttonTicked( 0 ) or self.inputManager.interactKeyTicked():
            self.done = True

        if not self.inputManager.isRunning():
            self.done = True

        # Keyboard actions
        if self.inputManager.keyTicked( annchienta.SDLK_DOWN ):
            self.selectedOptionIndex += 1
        elif self.inputManager.keyTicked( annchienta.SDLK_UP ):
            self.selectedOptionIndex -= 1
        elif self.inputManager.keyTicked( annchienta.SDLK_LEFT ):
            self.selectedOptionIndex -= self.rows
        elif self.inputManager.keyTicked( annchienta.SDLK_RIGHT ):
            self.selectedOptionIndex += self.rows

        if self.inputManager.isMouseMoved():

            sx, sy = self.x+self.sceneManager.getMargin(), self.y+self.sceneManager.getMargin()+ self.sceneManager.getItalicsFont().getLineHeight()
            for x in range(self.columns):
                for y in range(self.rows):
                    idx = x*self.rows+y
                    if idx<len(self.options):
                        o = self.options[ idx ]
                        # Do not select when not enabled, else, check for hover
                        if o.isEnabled() and self.inputManager.hover( sx+x*(self.longest+self.sceneManager.getMargin()), sy+y*self.sceneManager.getDefaultFont().getLineHeight(), sx+(x+1)*(self.longest+self.sceneManager.getMargin()), sy+(y+1)*self.sceneManager.getDefaultFont().getLineHeight() ):
                            self.selectedOption = o
                            self.selectedOptionIndex = self.getOptionIndex( o )
 
        self.selectedOptionIndex = self.selectedOptionIndex % len(self.options)
        self.selectedOption = self.options[self.selectedOptionIndex]


    def render( self ):

        # Draw box for the menu
        self.sceneManager.drawBox( self.x, self.y, self.x+self.width, self.y+self.height )
        self.videoManager.push()

        # Draw title
        self.videoManager.translate( self.x, self.y )
        self.videoManager.drawStringCentered( self.sceneManager.getItalicsFont(), self.name.capitalize(), self.width/2, self.sceneManager.getMargin() )

        # Move to the start of the items
        self.videoManager.translate( self.sceneManager.getMargin(), self.sceneManager.getMargin()+ self.sceneManager.getItalicsFont().getLineHeight() )

        # Render all items
        for x in range(self.columns):
            for y in range(self.rows):
                idx = x*self.rows+y
                if idx<len(self.options):
                    o = self.options[ idx ]
                    if o is self.selectedOption:
                        if o.isEnabled():
                            self.sceneManager.activeColor()
                        else:
                            # Item is selected but not enabled, draw in red
                            # or something
                            self.sceneManager.attentionColor()
                    else:
                        if o.isEnabled():
                            self.sceneManager.inactiveColor()
                        else:
                            self.sceneManager.disabledColor()
                    self.videoManager.drawString( self.sceneManager.getDefaultFont(), o.name.capitalize(), x*(self.longest+self.sceneManager.getMargin()), y*self.sceneManager.getDefaultFont().getLineHeight() )

        self.videoManager.pop()

        self.sceneManager.defaultColor()

        # Render tooltip
        if self.selectedOption is not None:
            if self.selectedOption.toolTip is not None:
                self.videoManager.push()

                # Count the lines we have to draw
                lines = self.selectedOption.toolTip.split('\n')

                # Calculate tooltip height
                h = self.sceneManager.getMargin()*2+self.sceneManager.getDefaultFont().getLineHeight()*len(lines)

                # Calculate tooltip y
                y = self.sceneManager.getMargin() if self.toolTipOnTop else self.videoManager.getScreenHeight()-self.sceneManager.getMargin()-h

                # Draw the tooltip
                self.sceneManager.drawBox( self.sceneManager.getMargin(), y, self.videoManager.getScreenWidth()-self.sceneManager.getMargin(), y+h )
                self.videoManager.translate( 0, y+self.sceneManager.getMargin() )

                for line in lines:
                    self.videoManager.drawString( self.sceneManager.getDefaultFont(), str(line), self.sceneManager.getMargin()*2, 0 )
                    self.videoManager.translate( 0, self.sceneManager.getDefaultFont().getLineHeight() )

                self.videoManager.pop()

