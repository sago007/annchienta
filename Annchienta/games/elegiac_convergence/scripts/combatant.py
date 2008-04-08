import annchienta
import scene

class Attribute:
    name = "name"
    value = 0

    def __init__( self, name, value ):
        self.name = name.lower()
        self.value = int(value)

class Status:

    attributes = []

    def __init__( self, element ):
        self.attributes = []

        keys = element.attributes.keys()
        for k in keys:
            attr = element.attributes[k]
            self.attributes += [Attribute(attr.name, attr.value)]

    def writeTo( self, element ):

        for a in self.attributes:
            element.setAttribute( a.name, str(a.value) )

    def get( self, name ):

        for a in attributes:
            if a.name == name.lower():
                return a.value

    def set( self, name, value ):

        for a in attributes:
            if a.name == name.lower():
                a.value = value
                return

        # if not found, append an attribute
        attributes += [Attribute(name,value)]

    def add( self, name, value ):

        for a in attributes:
            if a.name == name.lower():
                a.value += value
                return

        # if not found, append an attribute
        attributes += [Attribute(name,value)]

class Combatant:

    videoManager = annchienta.getVideoManager()
    sceneManager = scene.getSceneManager()

    name = "Name"
    health = 6
    delay = 6
    hostile = False
    status = None

    def __init__( self, element ):

        self.name = element.getAttribute("name")

        spriteElement = element.getElementsByTagName("sprite")[0]
        if spriteElement.hasAttribute("x1"):
            self.setSprite( str(spriteElement.getAttribute("filename")), int(spriteElement.getAttribute("x1")), int(spriteElement.getAttribute("y1")), int(spriteElement.getAttribute("x2")), int(spriteElement.getAttribute("y2")) )
        else:
            self.setSprite( str(spriteElement.getAttribute("filename")) )

        statusElement = element.getElementsByTagName("status")[0]
        self.status = Status( statusElement )

        self.delay = 6

    def draw( self ):

        x = 40 if self.hostile else self.videoManager.getScreenWidth()-40-self.sprite.getWidth()

        if self.sx1 is None:
            self.videoManager.drawSurface( self.sprite, x, 40 )
        else:
            self.videoManager.drawSurface( self.sprite, x, 40, self.sx1, self.sy1, self.sx2, self.sy2 )

    def setSprite( self, fname, x1=None, y1=None, x2=None, y2=None ):
        self.spriteFileName = fname
        self.sprite = annchienta.Surface( self.spriteFileName )
        self.sx1, self.sy1 = x1, y1
        self.sx2, self.sy2 = x2, y2

    def takeTurn( self ):
        self.delay += 6

class Ally(Combatant):

    def __init__( self, element ):

        Combatant.__init__( self, element )
        self.hostile = False
        self.buildMenu()

    def buildMenu( self ):
        pass

    def takeTurn( self ):
        self.sceneManager.info( self.name.capitalize()+" fights! (delay: "+str(self.delay)+")" )
        self.delay += 6

class Enemy(Combatant):

    def __init__( self, element ):

        Combatant.__init__( self, element )
        self.hostile = True

    def takeTurn( self ):
        self.sceneManager.info( self.name.capitalize()+" acts! (delay: "+str(self.delay)+")" )
        self.delay += 6
