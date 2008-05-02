import annchienta
import random

## \brief Handles scene tasks.
#
#  This class is used for drawing scene elements such as dialogs.
#  Note that this is an optional python class, meaning it can be left
#  out, and that you can easily customize it.
#
#  Uses video buffer 7.
class SceneManager:

    margin = 6
    defaultFont, italicsFont = None, None
    boxTextures = []

    engine = annchienta.getEngine()
    videoManager = annchienta.getVideoManager()
    inputManager = annchienta.getInputManager()
    audioManager = annchienta.getAudioManager()
    cacheManager = annchienta.getCacheManager()
    mapManager = annchienta.getMapManager()

    def waitForKey( self ):
        self.videoManager.storeBuffer(7)
        done = False
        self.inputManager.update()
        while self.inputManager.running() and not self.ticked( self.confirmKeys+self.cancelKeys ):
            self.inputManager.update()
            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.videoManager.end()

        self.mapManager.resync()

    def defaultColor( self ):
        self.videoManager.setColor(255,255,255)

    def activeColor( self ):
        self.videoManager.setColor(255,255,0)

    def inactiveColor( self ):
        self.videoManager.setColor(170,170,170)

    ## \brief Draw a box.
    #
    #  A box is the main GUI element. You can customize the box layout
    #  by changing bitmaps.
    def drawBox( self, x1, y1, x2, y2 ):
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
            self.videoManager.drawPattern( self.boxTextures[7], x1+self.boxTextures[7].getWidth(), y2-self.boxTextures[7].getHeight(), x2-self.boxTextures[8].getWidth(), y2 )
            self.videoManager.drawPattern( self.boxTextures[3], x1, y1+self.boxTextures[0].getHeight(), x1+self.boxTextures[3].getWidth(), y2-self.boxTextures[6].getHeight() )
            self.videoManager.drawPattern( self.boxTextures[5], x2-self.boxTextures[5].getWidth(), y1+self.boxTextures[2].getHeight(), x2, y2-self.boxTextures[8].getHeight() )

            # Draw the main texture as pattern.
            self.videoManager.drawPattern( self.boxTextures[4], x1+self.boxTextures[0].getWidth(), y1+self.boxTextures[0].getHeight(), x2-self.boxTextures[8].getWidth(), y2-self.boxTextures[8].getHeight() )

    ## \brief Renders justified text.
    #
    #  \return The height of the rendered text.
    def renderTextInArea( self, text, x1, y1, x2, font ):
        paragraphs = text.split('\n')
        spaceWidth = font.getStringWidth(' ')
        maxWidth = x2 - x1
        oy1 = y1
        for paragraph in paragraphs:
            words = paragraph.split()
            lineWords = []
            totalWidth = 0
            for word in words:
                if totalWidth+font.getStringWidth(word)+spaceWidth < maxWidth:
                    totalWidth += font.getStringWidth(word) + spaceWidth
                    lineWords.append( word )
                else:
                    if len(lineWords)<=0:
                        break
                    totalWidth = -spaceWidth
                    for w in lineWords:
                        totalWidth += font.getStringWidth(w)
                    actualSpaceWidth = (maxWidth-totalWidth)/(len(lineWords))
                    x = x1
                    for w in lineWords:
                        self.videoManager.drawString( font, w, x, y1 )
                        x += font.getStringWidth(w) + actualSpaceWidth
                    y1 += font.getLineHeight()
                    totalWidth = font.getStringWidth(word)
                    lineWords = [ word ]
            x = x1
            for w in lineWords:
                self.videoManager.drawString( font, w, x, y1 )
                x += font.getStringWidth(w) + spaceWidth
            y1 += font.getLineHeight()
        # Return the height elapsed.
        return y1-oy1

    ## \brief Display some text.
    #
    #  \param text The text to be displayed.
    def text( self, text, font=None ):

        font = self.defaultFont if font is None else font

        text = str(text)

        self.inputManager.update()
        self.videoManager.storeBuffer(7)

        while self.inputManager.running() and not self.inputManager.buttonTicked(0):

            self.inputManager.update()

            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
            self.videoManager.setClippingRectangle( 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 3*self.margin, 110-self.margin )
            self.defaultColor()
            height = self.renderTextInArea( text, 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 3*self.margin, font )
            height -= 110 - font.getLineHeight()
            self.videoManager.disableClipping()
            self.videoManager.end()

        self.videoManager.restoreBuffer(7)
        self.mapManager.resync()

    def thoughts( self, text ):

        text = str(text)
        scroll = 0
        self.inputManager.update()
        self.videoManager.storeBuffer(7)
        while self.inputManager.running() and not self.inputManager.buttonTicked(0):

            self.inputManager.update()

            self.videoManager.begin()
            self.videoManager.setColor(0,0,0)
            self.videoManager.drawRectangle(0,0,self.videoManager.getScreenWidth(),self.videoManager.getScreenHeight())
            self.defaultColor()
            self.renderTextInArea( text, 2*self.margin, 100, self.videoManager.getScreenWidth() - 2*self.margin, self.italicsFont )
            self.videoManager.end()

        self.videoManager.restoreBuffer(7)
        self.mapManager.resync()

    ## \brief Display some info.
    #
    #  \param text The text to be displayed.
    def info( self, text, timeOut=800 ):

        text = str(text)
        self.inputManager.update()
        self.videoManager.storeBuffer(7)

        start = self.engine.getTicks()

        done = False

        while not done:

            self.inputManager.update()

            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, self.margin*3+self.defaultFont.getLineHeight() )
            self.defaultColor()
            self.videoManager.drawString( self.defaultFont, text, 2*self.margin, 2*self.margin )
            self.videoManager.end()

            if not self.inputManager.running() or self.inputManager.buttonTicked( 0 ):
                done = True

            if timeOut is not None:
                if self.engine.getTicks() > start+timeOut:
                    done = True

        self.videoManager.restoreBuffer(7)
        self.mapManager.resync()


    ## \brief lets someone say something.
    #
    def speak(self, object, text):

        self.mapManager.cameraPeekAt( object, True )
        self.videoManager.begin()
        self.mapManager.renderFrame()
        self.text( object.getName().capitalize() + ":\n" + text, self.defaultFont )

    def chat( self, speaker, intro, answers ):

        if speaker is not None:
            self.mapManager.cameraPeekAt( speaker, True )
        self.videoManager.begin()
        self.mapManager.renderFrame()

        selected = 0
        self.inputManager.update()
        self.videoManager.storeBuffer(7)

        intro = (speaker.getName().capitalize()+":\n"+intro) if speaker is not None else intro

        done = False

        while self.inputManager.running() and not done:

            self.inputManager.update()

            y = 0

            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
            # Make sure everything goes in the box.
            self.videoManager.setClippingRectangle( 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 2*self.margin, 110-self.margin )
            self.defaultColor()
            height = self.renderTextInArea( intro, 2*self.margin, 2*self.margin+y, self.videoManager.getScreenWidth() - 2*self.margin, self.defaultFont )
            y += height+self.margin

            for i in range(len(answers)):

                if self.inputManager.hover( 2*self.margin, 2*self.margin+y, self.videoManager.getScreenWidth() - 2*self.margin, 2*self.margin+y+self.defaultFont.getLineHeight() ):
                    self.activeColor()
                    if self.inputManager.buttonTicked(0):
                        selected = i
                        done = True
                else:
                    self.inactiveColor()

                height = self.renderTextInArea( answers[i], 2*self.margin, 2*self.margin+y, self.videoManager.getScreenWidth() - 2*self.margin, self.defaultFont )
                y += height

            self.videoManager.disableClipping()
            self.videoManager.end()

        self.videoManager.setColor()
        self.videoManager.restoreBuffer(7)
        self.mapManager.resync()
        return selected

    def choose(self, title, answers):

        selected = 0
        done = False
        self.inputManager.update()
        self.videoManager.storeBuffer(7)

        while self.inputManager.running() and not done:

            self.inputManager.update()

            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
            self.defaultColor()
            y = self.margin*2
            self.videoManager.drawString( self.defaultFont, title, self.margin*2, y )
            y += self.defaultFont.getLineHeight()
            for i in range(len(answers)):

                if self.inputManager.hover( self.margin*2, y, self.videoManager.getScreenWidth()-self.margin*2, y+self.defaultFont.getLineHeight() ):
                    self.activeColor()
                    if self.inputManager.buttonTicked(0):
                        selected = i
                        done = True
                else:
                    self.inactiveColor()

                self.videoManager.drawString( self.defaultFont, answers[i], self.margin*2, y )
                y += self.defaultFont.getLineHeight()
            self.videoManager.end()

        self.videoManager.setColor()
        self.videoManager.restoreBuffer(7)
        self.mapManager.resync()
        return answers[selected]


    ## \moves someone.
    #
    def move(self, object, point ):

        self.inputManager.update()
        self.inputManager.setInputMode( annchienta.CinematicMode )

        while self.inputManager.running() and object.stepTo(point):

            self.mapManager.update(False)
            self.inputManager.update()

            self.mapManager.cameraPeekAt( object, True )

            self.videoManager.begin()
            self.mapManager.renderFrame()
            self.videoManager.end()

        self.inputManager.setInputMode( annchienta.InteractiveMode )
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

    ## \brief Ends a dialog.
    #
    def quitDialog( self ):
        for object in self.objectsInDialog:
            object.freeze(False)

    ## \fades
    #
    def fadeOut( self ):
        ms = 500
        start = self.engine.getTicks()
        self.videoManager.storeBuffer(7)
        while self.engine.getTicks() < start+ms:
            alpha = float(self.engine.getTicks() - start)/float(ms)*255.0
            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.videoManager.setColor(0,0,0,int(alpha))
            self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.videoManager.getScreenHeight() )
            self.videoManager.end()
        self.mapManager.resync()

    def rotateEffect( self, duration=1500 ):
        start = self.engine.getTicks()
        self.videoManager.storeBuffer(7)
        while self.engine.getTicks() < start+duration:
            factor = float(self.engine.getTicks() - start)/float(duration)
            self.videoManager.begin()
            self.videoManager.translate( self.videoManager.getScreenWidth()/2, self.videoManager.getScreenHeight()/2 )
            self.videoManager.rotate( (factor+1.)*(factor+1.)*360. )
            self.videoManager.scale( factor*50., factor*50. )
            self.videoManager.translate( -self.videoManager.getScreenWidth()/2, -self.videoManager.getScreenHeight()/2 )
            self.videoManager.restoreBuffer(7)
            self.videoManager.end()
        self.mapManager.resync()

    def noise( self, duration=1000 ):
        start = self.engine.getTicks()
        self.videoManager.storeBuffer(7)
        s = self.cacheManager.getSound("sounds/noise.ogg")
        self.audioManager.playSound( s )
        while self.engine.getTicks() < start+duration and self.inputManager.running():
            self.videoManager.begin()
            r = random.randint(0,255)
            self.videoManager.setColor( r, r, r )
            self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.videoManager.getScreenHeight() )
            self.videoManager.end()
        self.videoManager.setColor()
        self.videoManager.restoreBuffer(7)
        self.mapManager.resync()

## \brief Init the SceneManager global instance.
#
#  You should call this function only once, usually at the
#  start of your game.
#
def initSceneManager():
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
