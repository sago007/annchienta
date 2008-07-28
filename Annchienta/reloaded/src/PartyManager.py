import annchienta
import xml.dom.minidom

## Manages the player, party, etc.
#
class PartyManager:

    def __init__( self ):
    
        # Get some references
        self.inputManager = annchienta.getInputManager()
        self.mapManager = annchienta.getMapManager()

        # Set variables
        self.records = []
        self.lastMaps = []
        self.currentMap = 0

    def free( self ):
        self.currentMap.removeObject(self.player)
        self.currentMap = 0
        self.team = 0
        self.records = []
        self.mapManager.setNullMap()

    def load( self, filename ):
        self.filename = filename
        self.document = xml.dom.minidom.parse( self.filename )

        # Let's asume this is a valid file and
        # the needed elements are there.

        # <PLAYER>
        playerElement = self.document.getElementsByTagName("player")[0]
        self.player = annchienta.Person( str(playerElement.getAttribute("name")), str(playerElement.getAttribute("xmlfile")) )
        point = None
        if playerElement.hasAttribute("isox"):
            point = annchienta.Point( annchienta.IsometricPoint, int(playerElement.getAttribute("isox")), int(playerElement.getAttribute("isoy")) )
        if playerElement.hasAttribute("tilex"):
            point = annchienta.Point( annchienta.TilePoint, int(playerElement.getAttribute("tilex")), int(playerElement.getAttribute("tiley")) )
        self.player.setPosition( point )

        # <TEAM>
        teamElement = self.document.getElementsByTagName("team")[0]
        self.team = map( lambda e: combatant.Ally(e), teamElement.getElementsByTagName("combatant") )

        # <RECORDS>
        recordsElement = self.document.getElementsByTagName("records")[0]
        self.records = recordsElement.firstChild.data.split()

        # <MAP>
        # Load this after <RECORDS> because <RECORDS> might influence <MAP>.
        mapElement = self.document.getElementsByTagName("map")[0]
        self.currentMap = annchienta.Map( str(mapElement.getAttribute("filename")) )
        self.currentMap.setCurrentLayer( int(mapElement.getAttribute("layer")) )
        self.mapManager.setCurrentMap( self.currentMap )

        # Stuff to do when everything is loaded
        self.player.setInputControl()
        self.currentMap.addObject( self.player )
        self.mapManager.cameraFollow( self.player )
        self.inputManager.setInputControlledPerson( self.player )

    def save( self, filename=None ):

        self.filename = self.filename if filename is None else filename

        self.update()
        file = open( self.filename, "wb" )
        file.write( self.document.toprettyxml() )
        file.close()

    # Creates new xml document
    def update( self ):

        # Clear our map cache.
        self.lastMaps = []

        self.document = xml.dom.minidom.Document()
        partyElement = self.document.createElement("party")
        self.document.appendChild( partyElement )

        # <PLAYER>
        playerElement = self.document.createElement("player")
        player = self.inputManager.getInputControlledPerson()
        playerElement.setAttribute( "name", player.getName() )
        playerElement.setAttribute( "xmlfile", player.getXmlFile() )
        point = player.getPosition()
        point.convert( annchienta.IsometricPoint )
        playerElement.setAttribute( "isox", str(point.x) )
        playerElement.setAttribute( "isoy", str(point.y) )
        partyElement.appendChild( playerElement )

        # <MAP>
        mapElement = self.document.createElement("map")
        currentMap = self.mapManager.getCurrentMap()
        mapElement.setAttribute("filename", currentMap.getFileName() )
        mapElement.setAttribute("layer", str(currentMap.getCurrentLayerIndex()) )
        partyElement.appendChild( mapElement )

        # <RECORDS>
        recordsElement = self.document.createElement("records")
        data = ""
        for r in self.records:
            data += r+" "
        dataNode = self.document.createTextNode( data )
        recordsElement.appendChild( dataNode )
        partyElement.appendChild( recordsElement )

        # <TEAM>
        teamElement = self.document.createElement("team")
        for c in self.team:
            combatantElement = self.document.createElement("combatant")
            combatantElement.setAttribute( "name", c.name )

            spriteElement = self.document.createElement("sprite")
            spriteElement.setAttribute( "filename", c.spriteFileName )
            spriteElement.setAttribute( "x1", str(c.sx1) )
            spriteElement.setAttribute( "y1", str(c.sy1) )
            spriteElement.setAttribute( "x2", str(c.sx2) )
            spriteElement.setAttribute( "y2", str(c.sy2) )
            combatantElement.appendChild( spriteElement )

            statusElement = self.document.createElement("status")
            c.status.writeTo( statusElement )
            combatantElement.appendChild( statusElement )

            strategiesElement = self.document.createElement("strategies")
            data = ""
            for s in c.strategies:
                data += s+" "
            dataNode = self.document.createTextNode( data )
            strategiesElement.appendChild( dataNode )
            combatantElement.appendChild( strategiesElement )

            experienceElement = self.document.createElement("experience")
            c.experience.writeTo( experienceElement )
            combatantElement.appendChild( experienceElement )

            growthElement = self.document.createElement("growth")
            c.growth.writeTo( growthElement )
            combatantElement.appendChild( growthElement )

            teamElement.appendChild( combatantElement )

        partyElement.appendChild( teamElement )

    def addRecord( self, record ):
        if not self.hasRecord(record):
            self.records.append( record.lower() )

    def hasRecord( self, record ):
        return record.lower() in self.records

    def changeMap( self, newMapFileName, newPosition = annchienta.Point(annchienta.TilePoint, 2, 2 ), newLayer = 0, fade=True ):

        if fade:
            self.sceneManager.fadeOut()

        self.player.setPosition( newPosition )
        self.currentMap.removeObject( self.player )
        self.lastMaps += [self.currentMap]
        self.currentMap = annchienta.Map( newMapFileName )
        self.currentMap.setCurrentLayer( newLayer )
        self.currentMap.addObject( self.player )
        self.mapManager.setCurrentMap( self.currentMap )

        # Because loading a map can take some time:
        self.mapManager.resync()

    def changeLayer( self, index, newPosition = annchienta.Point( annchienta.TilePoint, 2, 2 ), fade = True ):
        if fade:
            self.sceneManager.fadeOut()
        self.player.setPosition( newPosition )
        self.currentMap.removeObject( self.player )
        self.currentMap.setCurrentLayer( index )
        self.currentMap.addObject( self.player )

        # Because changing a layer can take some time:
        self.mapManager.resync()

    def refreshMap( self ):
        pos = self.player.getPosition()
        self.changeMap( self.currentMap.getFileName(), pos, 0, False )

    def heal( self ):
        for c in self.team:
            c.status.set("health", c.status.get("maxhealth") )

def initPartyManager():
    global globalPartyManagerInstance
    globalPartyManagerInstance = PartyManager()

def getPartyManager():
    return globalPartyManagerInstance

