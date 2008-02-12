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
        #self.defaultFont
        self.boxTextures = []

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

    def renderTextInArea( self, text, x1, y1, x2, font ):
        paragraphs = text.split('\n')
        spaceWidth = font.getStringWidth(' ')
        maxWidth = x2 - x1
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

    ## \brief Display come text.
    #
    #  \param text The text to be displayed.
    def text( self, text ):
        self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
        self.videoManager.setClippingRectangle( 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 2*self.margin, 110-self.margin )
        self.videoManager.setColor( 255, 255, 255, 255 )
        self.renderTextInArea( text, 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 2*self.margin, self.defaultFont )
        self.videoManager.disableClipping()


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
