import annchienta
import scene
import battle
import strategy
import random
import menu

class Attribute:
    name = "name"
    value = 0

    def __init__( self, name, value ):
        self.name = name.lower()
        self.value = int(value)

class Status:

    def __init__( self, element=None ):

        self.attributes = []

        if not element is None:
            keys = element.attributes.keys()
            for k in keys:
                attr = element.attributes[k]
                self.attributes += [Attribute(attr.name, attr.value)]

    def writeTo( self, element ):

        for a in self.attributes:
            element.setAttribute( a.name, str(a.value) )

    def get( self, name ):

        for a in self.attributes:
            if a.name == name.lower():
                return a.value

    def set( self, name, value ):

        for a in self.attributes:
            if a.name == name.lower():
                a.value = value
                return

        # if not found, append an attribute
        attributes += [Attribute(name,value)]

    def add( self, name, value ):

        for a in self.attributes:
            if a.name == name.lower():
                a.value += value
                return

        # if not found, append an attribute
        self.attributes += [Attribute(name,value)]

class Combatant:

    videoManager = annchienta.getVideoManager()
    inputManager = annchienta.getInputManager()

    name = "Name"
    health = 6
    delay = 6
    hostile = False
    status = None
    m_strategy = None
    m_battle = None

    def __init__( self, element ):

        self.battleManager = battle.getBattleManager()
        self.sceneManager = scene.getSceneManager()

        self.name = element.getAttribute("name")

        spriteElement = element.getElementsByTagName("sprite")[0]
        if spriteElement.hasAttribute("x1"):
            self.setSprite( str(spriteElement.getAttribute("filename")), int(spriteElement.getAttribute("x1")), int(spriteElement.getAttribute("y1")), int(spriteElement.getAttribute("x2")), int(spriteElement.getAttribute("y2")) )
        else:
            self.setSprite( str(spriteElement.getAttribute("filename")) )

        statusElement = element.getElementsByTagName("status")[0]
        self.status = Status( statusElement )

        strategiesElement = element.getElementsByTagName("strategies")[0]
        self.strategies = map( lambda s: s.lower(), strategiesElement.firstChild.data.split() )

        experienceElements = element.getElementsByTagName("experience")
        if len( experienceElements ):
            self.experience = Status( experienceElements[0] )
        else:
            self.experience = Status()

        self.delay = 6
        self.m_strategy = strategy.Strategy( None, self )

    def draw( self ):

        if self.sx1 is None:
            self.videoManager.drawSurface( self.sprite, self.x, self.y )
        else:
            self.videoManager.drawSurface( self.sprite, self.x, self.y, self.sx1, self.sy1, self.sx2, self.sy2 )

    def setSprite( self, fname, x1=None, y1=None, x2=None, y2=None ):
        self.spriteFileName = fname
        self.sprite = annchienta.Surface( self.spriteFileName )
        self.sx1, self.sy1 = x1, y1
        self.sx2, self.sy2 = x2, y2

    def getSize( self ):
        if self.sx1 is None:
            return self.sprite.getWidth(), self.sprite.getHeight()
        else:
            return (self.sx2-self.sx1), (self.sy2-self.sy1)

    def setPosition( self, x, y ):
        self.posX, self.posY = x, y
        self.x, self.y = x, y

    def takeTurn( self ):

        if self.m_strategy.turns <= 0:
            self.m_strategy = self.createStrategy()

        if self.inputManager.running():
            self.m_strategy.control()

    def createStrategy( self ):

        # Select a random one.
        n = self.strategies[ random.randint(0, len(self.strategies)-1 ) ]
        s = strategy.getStrategy( n )
        return s( self.m_battle, self )

class Ally(Combatant):

    def __init__( self, element ):

        Combatant.__init__( self, element )

        experienceElements = element.getElementsByTagName("experience")
        if len(experienceElements):
            self.experience = Status( experienceElements[0] )
        else:
            self.experience = Status()

        self.hostile = False
        self.buildMenu()

    def buildMenu( self ):

        self.menu = menu.Menu( str(self.name.capitalize()), "Select behaviour for your combatant." )
        options = []
        for sn in self.strategies:
            s = strategy.getStrategy( sn )
            added = False
            for sub in options:
                if sub.name == s.category and not added:
                    sub.options += [menu.MenuItem( s.name, s.description )]
                    added = True
            if not added:
                sub = menu.Menu( s.category, s.category.capitalize()+"-based strategies." )
                sub.options += [menu.MenuItem( s.name, s.description )]
                options += [sub]

        for sub in options:
            sub.setOptions()

        self.menu.setOptions( options )
        self.menu.leftBottom()

    def createStrategy( self ):
        a = None
        while a is None and self.inputManager.running():
            a = self.menu.pop()

        if self.inputManager.running():
            s = strategy.getStrategy( a.name )

            # Add experience for ths chosen strategy.
            self.experience.add( a.name, 1 )

            return s( self.m_battle, self )
        else:
            return None

class Enemy(Combatant):

    def __init__( self, element ):

        Combatant.__init__( self, element )
        self.hostile = True

