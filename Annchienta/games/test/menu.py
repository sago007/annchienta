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
    options = []
    selectedItem = None
    width, height = 0, 0
    x, y = 0, 0
    toolTipOnTop = True

    def __init__( self, name, toolTip=None ):
        MenuItem.__init__( self, name, toolTip )
        self.inputManager = annchienta.getInputManager()
        self.videoManager = annchienta.getVideoManager()
        self.mapManager = annchienta.getMapManager()
        self.sceneManager = scene.getSceneManager()

    def setOptions( self, options ):
        self.options = options
        names = map( lambda o: o.name, options ) + [self.name]
        longest = max( map( lambda n: self.sceneManager.defaultFont.getStringWidth(n), names ) )
        self.width = longest + 5*self.sceneManager.margin
        self.height = len(options)*self.sceneManager.defaultFont.getLineHeight() + self.sceneManager.italicsFont.getLineHeight() + 2*self.sceneManager.margin

    def top( self ):
        self.toolTipOnTop = False
        self.y = self.sceneManager.margin
        self.x = (self.videoManager.getScreenWidth()-self.width)/2
        for m in self.options:
            if m.isMenu:
                m.top()

    def leftBottom( self ):
        self.toolTipOnTop = True
        self.y = self.videoManager.getScreenHeight()-self.height-self.sceneManager.margin
        self.x = self.sceneManager.margin
        for m in self.options:
            if m.isMenu:
                m.leftBottom()

    def pop( self ):

        self.videoManager.storeBuffer(6)

        self.inputManager.update()
        done = False
        canceled = False
        selected = 0
        self.selectedItem = self.options[selected]

        while not done:


            self.videoManager.begin()
            self.render()
            self.videoManager.end()

            self.inputManager.update()

            if self.sceneManager.ticked( self.sceneManager.nextKeys ):
                selected = selected+1 if selected+1<len(self.options) else 0
            if self.sceneManager.ticked( self.sceneManager.previousKeys ):
                selected = selected-1 if selected>0 else len(self.options)-1

            self.selectedItem = self.options[selected]

            if self.sceneManager.ticked( self.sceneManager.confirmKeys ):
                done = True

            if self.sceneManager.ticked( self.sceneManager.cancelKeys ):
                done = True
                canceled = True

            if not self.inputManager.running():
                done = True
                canceled = True

        self.mapManager.resync()

        self.videoManager.restoreBuffer(6)

        if canceled:
            return None
        else:
            if self.selectedItem.isMenu:
                sub = self.selectedItem.pop()
                if sub is None:
                    return self.pop()
                else:
                    return sub
            else:
                return self.selectedItem

    def render( self ):

        self.videoManager.restoreBuffer(6)

        self.videoManager.pushMatrix()

        self.videoManager.setColor( 255, 255, 255 )

        # Render tooltip
        if not self.selectedItem.toolTip is None:
            self.videoManager.pushMatrix()
            h = self.sceneManager.margin*2+self.sceneManager.defaultFont.getLineHeight()
            self.videoManager.translate( 0, self.sceneManager.margin if self.toolTipOnTop else self.videoManager.getScreenHeight()-self.sceneManager.margin*3-self.sceneManager.defaultFont.getLineHeight() )
            self.sceneManager.drawBox( self.sceneManager.margin, 0, self.videoManager.getScreenWidth()-self.sceneManager.margin, h )
            self.videoManager.drawString( self.sceneManager.defaultFont, self.selectedItem.toolTip, self.sceneManager.margin*2, self.sceneManager.margin )
            self.videoManager.popMatrix()

        # Render menu
        self.videoManager.translate( self.x, self.y )
        self.sceneManager.drawBox( 0, 0, self.width, self.height )

        self.videoManager.setColor( 230, 230, 230 )

        self.videoManager.drawStringCentered( self.sceneManager.italicsFont, self.name.capitalize(), self.width/2, self.sceneManager.margin )

        self.videoManager.translate( self.sceneManager.margin, self.sceneManager.margin+ self.sceneManager.italicsFont.getLineHeight() )
        self.videoManager.setColor( 255, 255, 255 )

        for o in self.options:
            self.videoManager.drawString( self.sceneManager.defaultFont, o.name.capitalize(), self.sceneManager.margin*2, 0 )
            if o is self.selectedItem:
                self.videoManager.drawTriangle( 0, 0, 0, self.sceneManager.defaultFont.getHeight(), self.sceneManager.margin, self.sceneManager.defaultFont.getHeight()/2 )
            self.videoManager.translate( 0, self.sceneManager.defaultFont.getLineHeight() )

        self.videoManager.popMatrix()

        self.videoManager.end()
