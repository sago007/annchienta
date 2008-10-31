import xml.dom.minidom
## Holds an action
#
class Action:

    def __init__( self, xmlElement ):
    
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
            self.type = powerElement.getAttribute("type")
            
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
            self.animation = str(animationElement.getAttribute("type"))
            if animationElement.hasAttribute("data"):
                self.animationData = str(animationElement.getAttribute("data"))
            else:
                self.animationData = None

            if animationElement.hasAttribute("sound"):
                self.animationSound = str(animationElement.getAttribute("sound"))
            else:
                self.animationSound = None
