import annchienta

## \brief Handles scene tasks.
#
#  This class is used for drawing scene elements such as dialogs.
#  Note that this is an optional python class, meaning it can be left
#  out, and that you can easily customize it.
class SceneManager:

    ## \brief Default contructor.
    #
    #  You should never call this constructor. Use initSceneManager() instead.
    def __init__( self ):
        self.margin = 6
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.mapManager = annchienta.getMapManager()
        #self.defaultFont
        self.boxTextures = []
        self.confirmKey = annchienta.SDLK_SPACE

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

    ## \brief Display come text.
    #
    #  \param text The text to be displayed.
    def text( self, text ):

        scroll = 0

        cx = self.mapManager.getCameraX()
        cy = self.mapManager.getCameraY()

        self.inputManager.setPersonInputEnabled(False)

        self.inputManager.update()

        while self.inputManager.running() and not self.inputManager.keyTicked( self.confirmKey ):

            self.mapManager.update()
            self.mapManager.setCameraX(cx)
            self.mapManager.setCameraY(cy)

            self.videoManager.begin()
            self.mapManager.renderFrame()
            self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
            self.videoManager.setClippingRectangle( 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 3*self.margin, 110-self.margin )
            self.videoManager.setColor( 255, 255, 255, 255 )
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

            if self.inputManager.keyTicked(annchienta.SDLK_DOWN) and scroll<height:
                scroll += 5
            if self.inputManager.keyTicked(annchienta.SDLK_UP) and scroll>0:
                scroll -= 5

        self.inputManager.setPersonInputEnabled(True)

    ## \brief lets someone say something.
    #
    def speak(self, object, text):

        self.mapManager.cameraPeekAt( object )
        self.text( object.getName().capitalize() + ":\n" + text )

    ## \moves someone.
    #
    def move(self, object, x, y):

        self.inputManager.update()
        self.inputManager.setPersonInputEnabled(False)

        while self.inputManager.running() and object.stepTo(x,y):

            self.mapManager.update()
            self.mapManager.cameraPeekAt( object )

            self.videoManager.begin()
            self.mapManager.renderFrame()
            self.videoManager.end()

        self.inputManager.setPersonInputEnabled(True)

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
