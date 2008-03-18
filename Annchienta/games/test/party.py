import annchienta
import xml.dom.minidom

class PartyManager:

    def __init__( self ):
        pass

    def load( self, filename ):
        self.filename = filename
        self.document = xml.dom.minidom.parse( self.filename )

    def save( self ):
        self.update()
        file = open( self.filename, "wb" )
        file.write( self.document.toprettyxml() )
        file.close()

    # Creates new xml document
    def update( self ):
        self.document = xml.dom.minidom.Document()
        self.partyElement = self.document.createElement("party")
        self.document.appendChild( self.partyElement )

        self.playerElement = self.document.createElement("player")
        player = annchienta.getInputManager().getInputControlledPerson()
        self.playerElement.setAttribute( "name", player.getName() )
        self.playerElement.setAttribute( "xmlfile", player.getXmlFile() )
        point = player.getPosition()
        point.convert( annchienta.IsometricPoint )
        self.playerElement.setAttribute( "isox", str(point.x) )
        self.playerElement.setAttribute( "isoy", str(point.y) )
        self.partyElement.appendChild( self.playerElement )

def initPartyManager():
    global globalPartyManagerInstance
    globalPartyManagerInstance = PartyManager()

def getPartyManager():
    return globalPartyManagerInstance

