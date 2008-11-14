import annchienta
import scene

class MenuItem:

    name = "Menu Item"
    toolTip = "Tool Tip"
    isMenu = False

    def __init__( self, name, toolTip=None ):
        self.name, self.toolTip = name, toolTip
        self.isMenuItem = True

## \brief A simple Menu.
#
#  Uses video buffer 6.
class Menu(MenuItem):

    isMenu = True
    width, height = 0, 0
    x, y = 0, 0
    toolTipOnTop = True

    maxItemsInColumn = 4

    def __init__( self, name, toolTip=None ):
        MenuItem.__init__( self, name, toolTip )
        self.inputManager = annchienta.getInputManager()
        self.videoManager = annchienta.getVideoManager()
        self.mapManager = annchienta.getMapManager()
        self.sceneManager = scene.getSceneManager()
        self.options = []

    def setOptions( self, options=None ):

        if not options is None:
            self.options = options

        self.rows = len(self.options) if len(self.options)<self.maxItemsInColumn else self.maxItemsInColumn
        self.columns = (len(self.options)/self.maxItemsInColumn)
        if len(self.options)%self.maxItemsInColumn:
            self.columns += 1

        names = map( lambda o: o.name, self.options ) + [self.name]
        self.longest = max( map( lambda n: self.sceneManager.defaultFont.getStringWidth(n.capitalize()), names ) )
        self.width = self.sceneManager.margin + (self.longest + self.sceneManager.margin)*self.columns
        self.height = self.rows*self.sceneManager.defaultFont.getLineHeight() + self.sceneManager.italicsFont.getLineHeight() + 2*self.sceneManager.margin

    def top( self ):
        self.toolTipOnTop = False
        self.y = self.sceneManager.margin
        self.x = (self.videoManager.getScreenWidth()-self.width)/2
        for m in self.options:
            if m.isMenu:
                m.top()

    def leftBottom( self ):
        self.toolTipOnTop = False
        self.y = self.videoManager.getScreenHeight()-self.height-self.sceneManager.margin*4-self.sceneManager.defaultFont.getLineHeight()
        self.x = self.sceneManager.margin
        for m in self.options:
            if m.isMenu:
                m.leftBottom()

    def pop( self ):

        self.videoManager.storeBuffer(6)

        self.inputManager.update()
        done = False
        self.clickedItem = None

        while not done and self.clickedItem is None:

            self.videoManager.clear()
            self.render()
            self.videoManager.flip()

            self.inputManager.update()

            if self.inputManager.buttonTicked( 1 ):
                done = True

            if not self.inputManager.running():
                done = True

        self.mapManager.resync()

        self.videoManager.setColor()
        self.videoManager.restoreBuffer(6)

        if self.clickedItem is None:
            return None
        else:
            if self.clickedItem.isMenu:
                sub = self.clickedItem.pop()
                if sub is None:
                    return self.pop()
                else:
                    return sub
            else:
                return self.clickedItem

    def render( self ):

        hover = None

        self.videoManager.restoreBuffer(6)
        self.sceneManager.drawBox( self.x, self.y, self.x+self.width, self.y+self.height )

        self.videoManager.pushMatrix()

        # Render menu
        self.videoManager.translate( self.x, self.y )
        self.videoManager.drawStringCentered( self.sceneManager.italicsFont, self.name.capitalize(), self.width/2, self.sceneManager.margin )

        self.videoManager.translate( self.sceneManager.margin, self.sceneManager.margin+ self.sceneManager.italicsFont.getLineHeight() )

        sx, sy = self.x+self.sceneManager.margin, self.y+self.sceneManager.margin+ self.sceneManager.italicsFont.getLineHeight()

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
            self.videoManager.pushMatrix()
            h = self.sceneManager.margin*2+self.sceneManager.defaultFont.getLineHeight()
            y = self.sceneManager.margin if self.toolTipOnTop else self.videoManager.getScreenHeight()-self.sceneManager.margin*3-self.sceneManager.defaultFont.getLineHeight()
            self.sceneManager.drawBox( self.sceneManager.margin, y, self.videoManager.getScreenWidth()-self.sceneManager.margin, y+h )
            self.videoManager.translate( 0, y )
            self.videoManager.drawString( self.sceneManager.defaultFont,hover.toolTip, self.sceneManager.margin*2, self.sceneManager.margin )
            self.videoManager.popMatrix()
