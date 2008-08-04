import annchienta
import xml.dom.minidom
import Ally

## Manages the player, party, etc.
#
class PartyManager:

    def __init__( self ):
    
        # Get some references
        self.inputManager = annchienta.getInputManager()
        self.mapManager = annchienta.getMapManager()

        # Set variables
        self.player = 0
        self.records = []
        self.lastMaps = []
        self.currentMap = 0

    def free( self ):
        self.currentMap.removeObject(self.player)
        self.currentMap = 0
        self.team = 0
        self.records = []
        self.mapManager.setNullMap()
        self.player = 0

    def load( self, filename ):

        # Store filename for later use
        self.filename = filename
        self.document = xml.dom.minidom.parse( self.filename )

        # Let's asume this is a valid file and
        # the needed elements are there.
        
        # Start by loading the records, because they are needed by the map
        recordsElement = self.document.getElementsByTagName("records")[0]
        self.records = str(recordsElement.firstChild.data).split()

        # Now we can safely load the map
        mapElement = self.document.getElementsByTagName("map")[0]
        self.currentMap = annchienta.Map( str(mapElement.getAttribute("filename")) )
        self.currentMap.setCurrentLayer( int(mapElement.getAttribute("layer")) )
        self.mapManager.setCurrentMap( self.currentMap )

        # Now that we have a map we can place the player in it
        playerElement = self.document.getElementsByTagName("player")[0]
        self.player = annchienta.Person( str(playerElement.getAttribute("name")), str(playerElement.getAttribute("config")) )
        self.player.setPosition( annchienta.Point( annchienta.IsometricPoint, int(playerElement.getAttribute("isox")), int(playerElement.getAttribute("isoy")) ) )

        # Add the player to the map and give him control
        self.currentMap.addObject( self.player )
        self.player.setInputControl()
        self.mapManager.cameraFollow( self.player )
        self.mapManager.cameraPeekAt( self.player, True )

        # Load the team
        teamElement = self.document.getElementsByTagName("team")[0]
        self.team = map( Ally.Ally, teamElement.getElementsByTagName("combatant") )

    def save( self, filename=None ):

        self.filename = self.filename if filename is None else filename

        self.generateDocument()
        file = open( self.filename, "wb" )
        file.write( self.document.toprettyxml() )
        file.close()

    # Creates new xml document
    def generateDocument( self ):

        # Clear our map cache.
        self.lastMaps = []

        # Create the document and main document node.
        self.document = xml.dom.minidom.Document()
        partyElement = self.document.createElement("party")
        self.document.appendChild( partyElement )

        # Append the records to the party node.
        recordsElement = self.document.createElement("records")
        # Create a text with the records
        text = reduce( lambda a, b: a+' '+b, self.records )
        textNode = self.document.createTextNode( text )
        recordsElement.appendChild( textNode )
        partyElement.appendChild( recordsElement )

        # Create an element for the map and add it to the party node
        mapElement = self.document.createElement("map")
        currentMap = self.mapManager.getCurrentMap()
        mapElement.setAttribute( "filename", currentMap.getFileName() )
        mapElement.setAttribute( "layer", str(currentMap.getCurrentLayerIndex()) )
        partyElement.appendChild( mapElement )

        # Create an element for the player
        playerElement = self.document.createElement("player")
        playerElement.setAttribute( "name", self.player.getName() )
        playerElement.setAttribute( "xmlfile", self.player.getXmlFile() )
        point = self.player.getPosition()
        point.convert( annchienta.IsometricPoint )
        playerElement.setAttribute( "isox", str(point.x) )
        playerElement.setAttribute( "isoy", str(point.y) )
        partyElement.appendChild( playerElement )

        # Create an element for the team
        teamElement = self.document.createElement("team")
        for combatant in self.team:
            combatantElement = self.document.createElement("combatant")
            
            # Set name
            combatantElement.setAttribute("name", combatant.name)

            # Set level info
            levelElement = self.document.createElement("level")
            for key in combatant.level:
                levelElement.setAttribute( str(key), str(combatant.level[key]) )
            combatantElement.appendChild( levelElement )

            # Set grades info
            gradesElement = self.document.createElement("grades")
            for key in combatant.grades:
                gradesElement.setAttribute( str(key), str(combatant.grades[key]) )
            combatantElement.appendChild( gradesElement )

            # Set primaryStats info
            primaryStatsElement = self.document.createElement("primarystats")
            for key in combatant.primaryStats:
                primaryStatsElement.setAttribute( str(key), str(combatant.primaryStats[key]) )
            combatantElement.appendChild( primaryStatsElement )
            
            # Set healthStats info
            healthStatsElement = self.document.createElement("healthstats")
            for key in combatant.healthStats:
                healthStatsElement.setAttribute( str(key), str(combatant.healthStats[key]) )
            combatantElement.appendChild( healthStatsElement )

            # Set weapon name
            weaponElement = self.document.createElement("weapon")
            weaponElement.setAttribute("name", str(combatant.weapon.name) )
            combatantElement.appendChild( weaponElement )

            # Set possible actions      
            actionsElement = self.document.createElement("actions")
            # Create a text with the actions
            text = reduce( lambda a, b: a+' '+b, map( lambda a: str(a.name), combatant.actions ) )
            textNode = self.document.createTextNode( text )
            actionsElement.appendChild( textNode )
            combatantElement.appendChild( actionsElement )

            # Set sprite info
            spriteElement = self.document.createElement("sprite")
            spriteElement.setAttribute( "filename", combatant.spriteFilename )
            spriteElement.setAttribute( "x1", str(combatant.sx1) )
            spriteElement.setAttribute( "x1", str(combatant.sy1) )
            spriteElement.setAttribute( "x1", str(combatant.sx2) )
            spriteElement.setAttribute( "x1", str(combatant.sy2) )
            combatantElement.appendChild( spriteElement )

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
            c.healthStats["hp"] = c.healthStats["mhp"]
            c.healthStats["mp"] = c.healthStats["mhp"]

def initPartyManager():
    global globalPartyManagerInstance
    globalPartyManagerInstance = PartyManager()

def getPartyManager():
    return globalPartyManagerInstance

