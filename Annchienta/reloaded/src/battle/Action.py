import xml.dom.minidom
## Holds an action
#
class Action:

    def __init__( self, xmlElement ):
    
        # Set our name and category
        self.name = xmlElement.getAttribute("name")
        self.category = xmlElement.getAttribute("category")
    
        # Create a dictionary describing the elemental properties
        self.elemental = {}
        elementalElement = xmlElement.getElementsByTagName("elemental")[0]
        for k in elementalElement.attributes.keys():
            self.elemental[k] = int(elementalElement.attributes[k].value)

        # Set factor and hit
        powerElement = xmlElement.getElementsByTagName("power")[0]
        self.factor = float( powerElement.getAttribute("factor") )
        self.hit = float( powerElement.getAttribute("hit") )
        
        # Set statusEffect and statusHit
        statusElement = xmlElement.getElementsByTagName("status")[0]
        self.statusEffect = statusElement.getAttribute("effect")
        self.statusHit = float( statusElement.getAttribute("hit") )
        
        # Set cost
        costElement = xmlElement.getElementsByTagName("cost")[0]
        self.cost = costElement.getAttribute("mp")
        
        # Set animation and animationData
        animationElement = xmlElement.getElementsByTagName("animation")[0]
        self.animation = animationElement.getAttribute("type")
        self.animationData = animationElement.getAttribute("data")

