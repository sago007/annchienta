import annchienta
import xml.dom.minidom
import AttackAnimation
import SpriteAnimation


## Holds an action
#
class Action:

    ## Create an Action based on an xml element.
    #  if you do not specify this element, you'll
    #  have to set things like a name and such by
    #  yourself.
    def __init__( self, xmlElement=None ):

        self.cacheManager = annchienta.getCacheManager()
   
        if xmlElement:

            # Set our name and category
            self.name = str(xmlElement.getAttribute("name"))
            self.category = str(xmlElement.getAttribute("category"))
            self.target = int(xmlElement.getAttribute("target"))
        
            # Get the description
            descriptionElement = xmlElement.getElementsByTagName("description")[0]
            self.description = str(descriptionElement.firstChild.data)
        
            # Set cost
            costElement = xmlElement.getElementsByTagName("cost")[0]
            self.cost = int(costElement.getAttribute("mp"))

            # Create a dictionary describing the elemental properties
            self.elemental = {}
            found = xmlElement.getElementsByTagName("elemental")
            if len(found):
                elementalElement = found[0]
                for k in elementalElement.attributes.keys():
                    self.elemental[k] = int(elementalElement.attributes[k].value)

            # Set factor, hit and type
            found = xmlElement.getElementsByTagName("power")
            if len(found):
                powerElement = found[0]
                self.factor = float( powerElement.getAttribute("factor") )
                self.hit = float( powerElement.getAttribute("hit") )
                self.type = str( powerElement.getAttribute("type") )
                
            # Set statusEffect and statusHit
            found = xmlElement.getElementsByTagName("status")
            if len(found):
                statusElement = found[0]
                self.statusEffect = str(statusElement.getAttribute("effect"))
                self.statusHit = float( statusElement.getAttribute("hit") )
                
            # Set animation and animationData
            found = xmlElement.getElementsByTagName("animation")
            if len(found):

                animationElement = found[0]

                sprite, sound = None, None

                if animationElement.hasAttribute("sprite"):
                    sprite = self.cacheManager.getSurface( str(animationElement.getAttribute("sprite")) )

                if animationElement.hasAttribute("sound"):
                    sound = self.cacheManager.getSound( str(animationElement.getAttribute("sound")) )

                type = str(animationElement.getAttribute("type"))

                if type=="attack":
                    self.animation = AttackAnimation.AttackAnimation( sprite, sound )
                elif type=="sprite":
                    self.animation = SpriteAnimation.SpriteAnimation( sprite, sound )
                else:
                    self.animation = None

    def getName( self ):
        return self.name

    def getCategory( self ):
        return self.category

    def hasTarget( self ):
        return self.target

    def getDescription( self ):
        return self.description

    def getCost( self ):
        return self.cost

    def hasElement( self, element ):
        if element in self.elemental:
            return self.elemental[ element ]
        else:
            return False

    def getElementList( self ):
        elementalList = []
        for element in self.elemental:
            if self.elemental[ element ]:
                elementalList.append( element )
        return elementalList

    def getFactor( self ):
        return self.factor

    def getHit( self ):
        return self.hit

    def getType( self ):
        return self.type

    def getStatusEffect( self ):
        return self.statusEffect

    def getStatusHit( self ):
        return self.statusHit

    def getAnimation( self ):
        return self.animation
