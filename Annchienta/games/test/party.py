import annchienta
import xml.dom.minidom

class PartyManager:

    records = []
    currentMap = 0

    def __init__( self ):
        self.inputManager = annchienta.getInputManager()
        self.mapManager = annchienta.getMapManager()

    def __del__(self):
        # So the player won't get deleted twice.
        self.currentMap.removeObject(self.player)

    def load( self, filename ):
        self.filename = filename
        self.document = xml.dom.minidom.parse( self.filename )

        # Let's asume this is a valid file and
        # the needed elements are there.
        mapElement = self.document.getElementsByTagName("map")[0]
        self.currentMap = annchienta.Map( str(mapElement.getAttribute("filename")) )
        self.currentMap.setCurrentLayer( int(mapElement.getAttribute("layer")) )
        self.mapManager.setCurrentMap( self.currentMap )

        playerElement = self.document.getElementsByTagName("player")[0]
        self.player = annchienta.Person( str(playerElement.getAttribute("name")), str(playerElement.getAttribute("xmlfile")) )
        point = annchienta.Point( annchienta.IsometricPoint, int(playerElement.getAttribute("isox")), int(playerElement.getAttribute("isoy")) )
        self.player.setPosition( point )
        self.player.setInputControl()
        self.currentMap.addObject( self.player )
        self.mapManager.cameraFollow( self.player )
        self.inputManager.setInputControlledPerson( self.player )

        recordsElement = self.document.getElementsByTagName("records")[0]
        self.records = recordsElement.firstChild.data.split()

    def save( self ):
        self.update()
        file = open( self.filename, "wb" )
        file.write( self.document.toprettyxml() )
        file.close()

    # Creates new xml document
    def update( self ):

        self.document = xml.dom.minidom.Document()
        partyElement = self.document.createElement("party")
        self.document.appendChild( partyElement )

        playerElement = self.document.createElement("player")
        player = self.inputManager.getInputControlledPerson()
        playerElement.setAttribute( "name", player.getName() )
        playerElement.setAttribute( "xmlfile", player.getXmlFile() )
        point = player.getPosition()
        point.convert( annchienta.IsometricPoint )
        playerElement.setAttribute( "isox", str(point.x) )
        playerElement.setAttribute( "isoy", str(point.y) )
        partyElement.appendChild( playerElement )

        mapElement = self.document.createElement("map")
        currentMap = self.mapManager.getCurrentMap()
        mapElement.setAttribute("filename", currentMap.getFileName() )
        mapElement.setAttribute("layer", str(currentMap.getCurrentLayerIndex()) )
        partyElement.appendChild( mapElement )

        recordsElement = self.document.createElement("records")
        data = ""
        for r in self.records:
            data += r+" "
        dataNode = self.document.createTextNode( data )
        recordsElement.appendChild( dataNode )
        partyElement.appendChild( recordsElement )

    def addRecord( self, record ):
        if not self.hasRecord(record):
            self.records.append( record.lower() )

    def hasRecord( self, record ):
        return record.lower() in self.records

    def changeMap( self, newMapFileName, newPosition = annchienta.Point(annchienta.TilePoint, 2, 2 ) ):
        self.player.setPosition( newPosition )
        self.currentMap.removeObject( self.player )
        self.lastMap = self.currentMap
        self.currentMap = annchienta.Map( newMapFileName )
        self.currentMap.addObject( self.player )
        self.mapManager.setCurrentMap( self.currentMap )

def initPartyManager():
    global globalPartyManagerInstance
    globalPartyManagerInstance = PartyManager()

def getPartyManager():
    return globalPartyManagerInstance

