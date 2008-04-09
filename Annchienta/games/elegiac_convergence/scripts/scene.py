import annchienta

## \brief Handles scene tasks.
#
#  This class is used for drawing scene elements such as dialogs.
#  Note that this is an optional python class, meaning it can be left
#  out, and that you can easily customize it.
#
#  Uses video buffer 7.
class SceneManager:

    margin = 6
    confirmKeys = [annchienta.SDLK_SPACE]
    cancelKeys = [annchienta.SDLK_BACKSPACE]
    nextKeys = [annchienta.SDLK_DOWN,annchienta.SDLK_RIGHT]
    previousKeys = [annchienta.SDLK_UP,annchienta.SDLK_LEFT]
    upKeys = [annchienta.SDLK_UP]
    downKeys = [annchienta.SDLK_DOWN]
    leftKeys = [annchienta.SDLK_LEFT]
    rightKeys = [annchienta.SDLK_RIGHT]
    defaultFont, italicsFont = None, None
    boxTextures = []

    engine = annchienta.getEngine()
    videoManager = annchienta.getVideoManager()
    inputManager = annchienta.getInputManager()
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

    def ticked( self, keys ):
        for k in keys:
            if self.inputManager.keyTicked(k):
                return True
        return False

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
    def text( self, text ):

        text = str(text)
        scroll = 0

        self.inputManager.update()
        self.videoManager.storeBuffer(7)

        while self.inputManager.running() and not self.ticked( self.confirmKeys ):

            self.inputManager.update()

            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
            self.videoManager.setClippingRectangle( 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 3*self.margin, 110-self.margin )
            self.defaultColor()
            height = self.renderTextInArea( text, 2*self.margin, 2*self.margin-scroll, self.videoManager.getScreenWidth() - 3*self.margin, self.defaultFont )
            height -= 110 - self.defaultFont.getLineHeight()
            self.videoManager.disableClipping()
            self.videoManager.pushMatrix()
            self.videoManager.translate( self.videoManager.getScreenWidth()-3*self.margin, 110-4*self.margin )
            if scroll>0:
                self.videoManager.drawTriangle( self.margin/2, 0, 0, self.margin, self.margin, self.margin )
            if scroll<height:
                self.videoManager.drawTriangle( 0, self.margin*2, self.margin/2, self.margin*3, self.margin, self.margin*2 )
            self.videoManager.popMatrix()
            self.videoManager.end()

            if self.ticked( self.nextKeys ) and scroll<height:
                scroll += self.defaultFont.getLineHeight()
            if self.ticked( self.previousKeys ) and scroll>0:
                scroll -= self.defaultFont.getLineHeight()

        self.videoManager.restoreBuffer(7)
        self.mapManager.resync()


    ## \brief Display some info.
    #
    #  \param text The text to be displayed.
    def info( self, text, timeOut=1200 ):

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

            if not self.inputManager.running() or self.ticked( self.confirmKeys ):
                done = True

            if not timeOut is None:
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
        self.text( object.getName().capitalize() + ":\n" + text )

    ## \moves someone.
    #
    def move(self, object, x, y):

        self.inputManager.update()
        self.inputManager.setPersonInputEnabled(False)

        while self.inputManager.running() and object.stepTo(x,y):

            self.mapManager.update(False)
            self.inputManager.update()

            self.mapManager.cameraPeekAt( object )

            self.videoManager.begin()
            self.mapManager.renderFrame()
            self.videoManager.end()

        self.inputManager.setPersonInputEnabled(True)

    def choose(self, title, answers):

        selected = 0
        self.inputManager.update()
        self.videoManager.storeBuffer(7)

        while self.inputManager.running() and not self.ticked( self.confirmKeys ):

            self.inputManager.update()

            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
            self.defaultColor()
            y = self.margin*2
            self.videoManager.drawString( self.defaultFont, title, self.margin*2, y )
            y += self.defaultFont.getLineHeight()
            for a in answers:
                if answers[selected] is a:
                    self.activeColor()
                else:
                    self.inactiveColor()
                self.videoManager.drawString( self.defaultFont, a, self.margin*2, y )
                y += self.defaultFont.getLineHeight()
            self.videoManager.end()

            if self.ticked( self.nextKeys ):
                selected = selected+1 if selected+1<len(answers) else 0
            if self.ticked( self.previousKeys ):
                selected = selected-1 if selected>=1 else len(answers)-1

        self.videoManager.setColor()
        self.videoManager.restoreBuffer(7)
        self.mapManager.resync()
        return answers[selected]

    def chat( self, intro, answers ):

        scroll = 0
        selected = 0
        self.inputManager.update()
        self.videoManager.storeBuffer(7)

        while self.inputManager.running() and not self.ticked( self.confirmKeys ):

            self.inputManager.update()

            y = 0

            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
            # Make sure everything goes in the box.
            self.videoManager.setClippingRectangle( 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 2*self.margin, 110-self.margin )
            self.defaultColor()
            height = self.renderTextInArea( intro, 2*self.margin, 2*self.margin-scroll+y, self.videoManager.getScreenWidth() - 2*self.margin, self.defaultFont )
            y += height

            yPositions = range(len(answers))

            for i in range(len(answers)):
                if selected is i:
                    self.activeColor()
                else:
                    self.inactiveColor()

                yPositions[i] = y

                height = self.renderTextInArea( answers[i], 2*self.margin, 2*self.margin-scroll+y, self.videoManager.getScreenWidth() - 2*self.margin, self.defaultFont )
                y += height

            yPositions.append(y)

            self.videoManager.disableClipping()
            self.videoManager.end()

            if self.ticked( self.nextKeys ):
                if selected+1<len(answers):
                    selected += 1

            if self.ticked( self.previousKeys ):
                if selected>0:
                    selected -= 1
                else:
                    scroll -= self.defaultFont.getLineHeight()

            while scroll>yPositions[selected]:
                scroll -= self.defaultFont.getLineHeight()

            while scroll+110-self.defaultFont.getLineHeight()<yPositions[selected+1]:
                scroll += self.defaultFont.getLineHeight()

        self.videoManager.setColor()
        self.videoManager.restoreBuffer(7)
        self.mapManager.resync()
        return selected

    ## \brief Inits a dialog.
    #
    def initDialog( self, objects ):
        for o in objects:
            o.freeze( True )
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

    def fadeIn( self ):
        ms = 500
        start = self.engine.getTicks()
        self.videoManager.storeBuffer(7)
        while self.engine.getTicks() < start+ms:
            alpha = 255. - float(self.engine.getTicks() - start)/float(ms)*255.0
            self.videoManager.begin()
            self.videoManager.restoreBuffer(7)
            self.videoManager.setColor(0,0,0,int(alpha))
            self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.videoManager.getScreenHeight() )
            self.videoManager.end()
        self.mapManager.resync()

    def rotateEffect( self ):
        ms = 4000
        start = self.engine.getTicks()
        self.videoManager.storeBuffer(7)
        while self.engine.getTicks() < start+ms:
            factor = float(self.engine.getTicks() - start)/float(ms)
            self.videoManager.begin()
            self.videoManager.translate( self.videoManager.getScreenWidth()/2, self.videoManager.getScreenHeight()/2 )
            self.videoManager.rotate( factor*360. )
            self.videoManager.scale( factor*100., factor*100. )
            self.videoManager.translate( -self.videoManager.getScreenWidth()/2, -self.videoManager.getScreenHeight()/2 )
            self.videoManager.restoreBuffer(7)
            self.videoManager.end()
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
