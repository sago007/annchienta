import annchienta

class SceneManager:

    def __init__( self ):
        self.margin = 6
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.defaultFont = annchienta.Font("editor/font.ttf", 14)

    def drawBox( self, x1, y1, x2, y2 ):
        self.videoManager.setColor( 100, 100, 150, 200 )
        self.videoManager.drawRectangle( x1, y1, x2, y2 )

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

    def text( self, text ):
        self.drawBox( self.margin, self.margin, self.videoManager.getScreenWidth() - self.margin, 110 )
        self.videoManager.setColor( 255, 255, 255, 255 )
        self.renderTextInArea( text, 2*self.margin, 2*self.margin, self.videoManager.getScreenWidth() - 2*self.margin, self.defaultFont )

def initSceneManager():
    global globalSceneManagerInstance
    globalSceneManagerInstance = SceneManager()

def getSceneManager():
    return globalSceneManagerInstance
