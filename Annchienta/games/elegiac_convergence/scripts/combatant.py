import annchienta

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

    name = "Name"
    health = 6
    delay = 6
    hostile = False
    status = None

    def __init__( self, element ):

        self.name = element.getAttribute("name")

        spriteElement = element.getElementsByTagName("sprite")[0]
        self.setSprite( str(spriteElement.getAttribute("filename")),
                        int(spriteElement.getAttribute("x1")),
                        int(spriteElement.getAttribute("y1")),
                        int(spriteElement.getAttribute("x2")),
                        int(spriteElement.getAttribute("y2")) )

        statusElement = element.getElementsByTagName("status")[0]
        self.status = Status( statusElement )

    def draw( self ):
        x = 40 if self.hostile else self.videoManager.getScreenWidth()-40-self.sprite.getWidth()
        self.videoManager.drawSurface( self.sprite, x, 40, self.sx1, self.sy1, self.sx2, self.sy2 )

    def setSprite( self, fname, x1, y1, x2, y2 ):
        self.spriteFileName = fname
        self.sprite = annchienta.Surface( self.spriteFileName )
        self.sx1, self.sy1 = x1, y1
        self.sx2, self.sy2 = x2, y2

    def takeTurn( self ):
        self.delay += 6

class Ally(Combatant):
    pass

class Enemy(Combatant):
    pass
