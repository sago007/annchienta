import annchienta

## \brief Handles scene tasks.
#
#  This class is used for drawing scene elements such as dialogs.
#  Note that this is an optional python class, meaning it can be left
#  out, and that you can easily customize it.
#
#  Uses video buffer 7.
class SceneManager(object):

    def __init__( self ):

        # Get references
        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.audioManager = annchienta.getAudioManager()
        self.cacheManager = annchienta.getCacheManager()
        self.mapManager = annchienta.getMapManager()

        # Load our assets
        self.defaultFont = annchienta.Font( "assets/regular.ttf", 14 )
        self.italicsFont = annchienta.Font( "assets/italics.ttf", 14 )
        self.largeDefaultFont = annchienta.Font( "assets/regular.ttf", 20 )
        self.largeItalicsFont = annchienta.Font( "assets/italics.ttf", 20 )
        self.boxTextures = map( lambda i: annchienta.Surface("assets/box"+str(i)+".png"), range(9) )

        self.margin = 6

    def waitForClick( self ):
        self.videoManager.storeBuffer(7)
        self.inputManager.update()
        while self.inputManager.isRunning() and not self.inputManager.buttonTicked(0) and not self.inputManager.interactKeyTicked():
            self.inputManager.update()
            self.videoManager.clear()
            self.videoManager.restoreBuffer(7)
            self.videoManager.flip()

        self.mapManager.resync()

    def defaultColor( self ):
        self.videoManager.setColor(255,255,255)

    def activeColor( self ):
        self.videoManager.setColor(255,255,0)

    def inactiveColor( self ):
        self.videoManager.setColor(170,170,170)

    def disabledColor( self ):
        self.videoManager.setColor(100,100,100)

    def attentionColor( self ):
        self.videoManager.setColor(255,0,0)

    def getMargin( self ):
        return self.margin

    def getDefaultFont( self ):
        return self.defaultFont

    def getItalicsFont( self ):
        return self.italicsFont

    def getLargeDefaultFont( self ):
        return self.largeDefaultFont

    def getLargeItalicsFont( self ):
        return self.largeItalicsFont

    ## \brief Draw a box.
    #  \param skipBlur Skip the background blur. This can speed up box drawing a lot.
    #  A box is the main GUI element. You can customize the box layout
    #  by changing bitmaps.
    def drawBox( self, x1, y1, x2, y2, skipBlur=False ):

        #self.videoManager.push()
        #self.videoManager.identity()
        if not skipBlur:
            self.videoManager.boxBlur( x1, y1, x2, y2 )
        #self.videoManager.pop()

        # If there are not enough textures, just draw a stupid simple box.
        if( len(self.boxTextures)<=8 ):
            self.videoManager.setColor( 100, 100, 150, 200 )
            self.videoManager.drawRectangle( x1, y1, x2, y2 )
            self.videoManager.setColor()
        else:
            # Draw the corner textures
            self.videoManager.drawSurface( self.boxTextures[0], x1, y1 )
            self.videoManager.drawSurface( self.boxTextures[2], x2-self.boxTextures[2].getWidth(), y1 )
            self.videoManager.drawSurface( self.boxTextures[6], x1, y2-self.boxTextures[6].getHeight() )
            self.videoManager.drawSurface( self.boxTextures[8], x2-self.boxTextures[2].getWidth(), y2-self.boxTextures[6].getHeight() )

            # Draw the side textures as patterns.
            self.videoManager.drawPattern( self.boxTextures[1], x1+self.boxTextures[0].getWidth(), y1, x2-self.boxTextures[2].getWidth(), y1+self.boxTextures[1].getHeight() )
            self.videoManager.drawPattern( self.boxTextures[7], x1+self.boxTextures[8].getWidth(), y2-self.boxTextures[7].getHeight(), x2-self.boxTextures[8].getWidth(), y2 )
            self.videoManager.drawPattern( self.boxTextures[3], x1, y1+self.boxTextures[0].getHeight(), x1+self.boxTextures[3].getWidth(), y2-self.boxTextures[6].getHeight() )
            self.videoManager.drawPattern( self.boxTextures[5], x2-self.boxTextures[5].getWidth(), y1+self.boxTextures[2].getHeight(), x2, y2-self.boxTextures[8].getHeight() )

            # Draw the main texture as pattern.
            self.videoManager.drawPattern( self.boxTextures[4], x1+self.boxTextures[0].getWidth(), y1+self.boxTextures[0].getHeight(), x2-self.boxTextures[8].getWidth(), y2-self.boxTextures[8].getHeight() )

    ## \brief Renders justified text.
    #
    #  \return The height of the rendered text.
    def renderTextInArea( self, text, x1, y1, x2, font ):
    
        # Split all lines
        paragraphs = text.split('\n')
        spaceWidth = font.getStringWidth(' ')
        maxWidth = x2 - x1
        oy1 = y1
        
        # Render all paragraphs
        for paragraph in paragraphs:
        
            # Divide into words
            words = paragraph.split()
            lineWords = [] # Words in a line
            totalWidth = 0
            
            # Render all words
            for word in words:
            
                # If the word fits within the max width, append it
                if totalWidth+font.getStringWidth(word)+spaceWidth < maxWidth:
                    totalWidth += font.getStringWidth(word) + spaceWidth
                    lineWords.append( word )
                else:
                    if len(lineWords)<=0:
                        break
                    totalWidth = -spaceWidth
                    for w in lineWords:
                        totalWidth += font.getStringWidth(w)
                        
                    # Adjust space width to have nicely justified text
                    actualSpaceWidth = (maxWidth-totalWidth)/(len(lineWords))
                    x = x1
                    
                    # Now actually draw the words
                    for w in lineWords:
                        self.videoManager.drawString( font, w, x, y1 )
                        x += font.getStringWidth(w) + actualSpaceWidth
                        
                    # Move to next line
                    y1 += font.getLineHeight()
                    totalWidth = font.getStringWidth(word)
                    lineWords = [ word ]
                    
            x = x1
            # Draw the last line of words
            for w in lineWords:
                self.videoManager.drawString( font, w, x, y1 )
                x += font.getStringWidth(w) + spaceWidth
            y1 += font.getLineHeight()

        # Return the height elapsed.
        return y1-oy1

    ## \brief Display some text.
    #
    #  \param text The text to be displayed.
    #  \param backgroundProcess The process handling the background. This object should have update( updateInputToo ) and draw() methods. This is usually the MapManager instance. If set to None, the initial background is kept.
    def text( self, text, backgroundProcess = annchienta.getMapManager(), italics=False ):

        # Make sure we're dealing with text
        text = str(text)

        # Choose font
        font = self.italicsFont if italics else self.defaultFont

        # No accidental clicks
        self.inputManager.update()
        
        if not backgroundProcess:
            self.videoManager.storeBuffer(7)

        while self.inputManager.isRunning() and not self.inputManager.buttonTicked(0) and not self.inputManager.interactKeyTicked():

            self.inputManager.update()

            # Update our background process
            if backgroundProcess:
                backgroundProcess.update(False)

            self.videoManager.clear()

            # Draw the background
            if backgroundProcess:
                backgroundProcess.draw()
            else:
                self.videoManager.restoreBuffer(7)

            self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
            self.videoManager.setClippingRectangle( 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 3*self.margin, 110-self.margin )
            self.defaultColor()
            height = self.renderTextInArea( text, 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 3*self.margin, font )
            height -= 110 - font.getLineHeight()
            self.videoManager.disableClipping()
            self.videoManager.flip()

        if not backgroundProcess:
            self.videoManager.restoreBuffer(7)

        self.mapManager.resync()


    ## \brief lets someone say something.
    #
    def speak(self, speaker, text, italics=False):

        # Quick backup, then look at speaker
        originalCameraFollow = self.mapManager.getCameraFollow()
        self.mapManager.cameraFollow( speaker )
        
        # Run text
        self.text( speaker.getName().capitalize() + ":\n" + text, annchienta.getMapManager(), italics )

        # Reset stuff
        self.mapManager.cameraFollow( originalCameraFollow )

    ## \moves someone.
    #
    def move(self, objects, points, followMover=False ):

        # Convert objects and points to lists if they aren't.
        if type(objects) is not type([]):
            objects = [objects]
            points = [points]

        self.inputManager.update()

        going = 1

        self.mapManager.resync()

        while self.inputManager.isRunning() and going:

            going = sum( map( lambda i: int(objects[i].stepTo(points[i])), range(len(objects)) ) )

            self.mapManager.update(False)
            self.inputManager.update()

            if followMover:
                self.mapManager.cameraPeekAt( objects[0], True )

            self.videoManager.clear()
            self.mapManager.renderFrame()
            self.videoManager.flip()

        self.mapManager.resync()

    ## \brief Inits a dialog.
    #
    def initDialog( self, objects ):
        for o in objects:
            o.freeze( True )
            o.setStandAnimation()
        for i in range(len(objects)):
            objects[i].lookAt( objects[(i+1)%len(objects)] )
        self.objectsInDialog = objects
        self.inputManager.setInputMode( annchienta.CinematicMode )

    ## \brief Ends a dialog.
    #
    def quitDialog( self ):
        for object in self.objectsInDialog:
            object.freeze(False)
        self.inputManager.setInputMode( annchienta.InteractiveMode )

    # Quick fade animation
    def fade( self, r=0, g=0, b=0, duration=1000 ):

        start = self.engine.getTicks()
        end = start + duration

        # Backup buffer
        self.videoManager.storeBuffer(7)

        while self.inputManager.isRunning() and self.engine.getTicks() < end:

            a = int(255.0*float( self.engine.getTicks()-start ) / float( duration ))

            self.videoManager.clear()
            self.videoManager.restoreBuffer(7)
            self.videoManager.setColor( r, g, b, a )
            self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.videoManager.getScreenHeight() )
            self.videoManager.flip()

            self.inputManager.update()

        # Fill it at the end
        self.videoManager.clear()
        self.videoManager.setColor( r, g, b, 255 )
        self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.videoManager.getScreenHeight() )
        self.videoManager.flip()

        self.mapManager.resync()

    # Game over animation
    def gameOver( self ):

        self.videoManager.setColor( 0, 0, 0, 150 )
        self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.videoManager.getScreenHeight() )
        self.videoManager.setColor( 255, 255, 255 )
        self.videoManager.drawStringCentered( self.largeItalicsFont, "Game Over", self.videoManager.getScreenWidth()/2, 120 )
        self.videoManager.flip()
        self.waitForClick()
        self.fade()

## \brief Init the SceneManager global instance.
#
#  You should call this function only once, usually at the
#  start of your game.
#
def init():
    global globalSceneManagerInstance
    globalSceneManagerInstance = SceneManager()

## \brief Obtain the VideoManager instance.
#
#  Use this function to get access to the SceneManager
#  instance anywhere.
#
#  \attention Since this is an optional class, call initSceneManager() once before using this function.
#
#  \return The global SceneManager instance.
def getSceneManager():
    return globalSceneManagerInstance

