import annchienta
import xml.dom.minidom
import Ally
import Inventory
import SceneManager

## Manages the player, party, etc.
#
class PartyManager:

    def __init__( self ):
    
        # Get some references
        self.engine = annchienta.getEngine()
        self.inputManager = annchienta.getInputManager()
        self.mapManager = annchienta.getMapManager()
        self.cacheManager = annchienta.getCacheManager()
        self.mathManager = annchienta.getMathManager()
        self.sceneManager = SceneManager.getSceneManager()

        # Set variables
        self.player = 0
        self.records = []
        self.inventory = 0
        self.lastMaps = []
        self.currentMap = 0
        self.chestObjects = []

        # Battle variables
        self.randomBattleDelay = self.mathManager.randInt(300,400)

    def free( self ):

        self.currentMap.removeObject(self.player)
        self.lastMaps += [self.currentMap]
        self.clearMapCache()
        self.currentMap = 0
        self.team = 0
        self.records = []
        self.inventory = 0
        self.mapManager.setNullMap()
        self.chestObjects = []
        self.player = 0

    def clearMapCache( self ):

        for map in self.lastMaps:
            self.freeMap( map )

        self.lastMaps = []

    def load( self, filename ):

        # Store filename for later use
        self.filename = filename
        self.document = xml.dom.minidom.parse( self.filename )

        # Let's asume this is a valid file and
        # the needed elements are there.
       
        # Load the playtime for profiling reasons
        playTimeElement = self.document.getElementsByTagName("playtime")[0]
        self.seconds = int(playTimeElement.getAttribute("seconds"))
 
        # Start by loading the records, because they are needed by the map
        recordsElement = self.document.getElementsByTagName("records")[0]
        self.records = str(recordsElement.firstChild.data).split()

        # Now we can safely load the map
        mapElement = self.document.getElementsByTagName("map")[0]
        self.currentMap = self.loadMap( str(mapElement.getAttribute("filename")) )
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

        # Load our inventory
        inventoryElement = self.document.getElementsByTagName("inventory")[0]
        self.inventory = Inventory.Inventory( inventoryElement )

        # Load the team
        teamElement = self.document.getElementsByTagName("team")[0]
        self.team = map( Ally.Ally, teamElement.getElementsByTagName("combatant") )

    # Saves the game to filename.
    def save( self, filename=None ):

        self.filename = self.filename if filename is None else filename
        self.generateDocument()
        file = open( self.filename, "wb" )
        file.write( self.document.toprettyxml() )
        file.close()

    # Creates new xml document with all save information
    # in it.
    def generateDocument( self ):

        # Clear our map cache.
        self.clearMapCache()

        # Create the document and main document node.
        self.document = xml.dom.minidom.Document()
        partyElement = self.document.createElement("party")
        self.document.appendChild( partyElement )

        # Add the playtime to the party node
        playTimeElement = self.document.createElement("playtime")
        playTimeElement.setAttribute( "seconds", str(self.seconds + self.engine.getTicks()/1000) )
        partyElement.appendChild( playTimeElement )

        # Append the records to the party node.
        recordsElement = self.document.createElement("records")
        # Create a text with the records
        text = " "
        for record in self.records:
            text += record + " "
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
        playerElement.setAttribute( "config", self.player.getXmlFile() )
        point = self.player.getPosition()
        point.convert( annchienta.IsometricPoint )
        playerElement.setAttribute( "isox", str(point.x) )
        playerElement.setAttribute( "isoy", str(point.y) )
        partyElement.appendChild( playerElement )

        # Append the inventory to the party node.
        inventoryElement = self.document.createElement("inventory")
        # Create a text with the records
        text = self.inventory.toXml()
        textNode = self.document.createTextNode( text )
        inventoryElement.appendChild( textNode )
        partyElement.appendChild( inventoryElement )

        # Create an element for the team
        teamElement = self.document.createElement("team")
        for combatant in self.team:
            combatantElement = self.document.createElement("combatant")
            combatant.writeToXML( combatantElement, self.document )
            teamElement.appendChild( combatantElement )

        partyElement.appendChild( teamElement )

    def addRecord( self, record ):
        if not self.hasRecord(record):
            self.records.append( record.lower() )

    def hasRecord( self, record ):
        return record.lower() in self.records

    def removeRecord( self, record ):
        if self.hasRecord( record ):
            self.records.remove( record )

    # Loads a map an extra stuff defined in the map, 
    # but not in the core engine.
    def loadMap( self, filename ):

        newMap = annchienta.Map( filename )

        # Get the pure xml
        document = xml.dom.minidom.parse( filename )

        # Go through layers
        layers = document.getElementsByTagName( "layer" )
        for i in range(len(layers)):

            # Set correct layer
            newMap.setCurrentLayer( i )            

            # Add chests
            chests = layers[i].getElementsByTagName( "chest" )

            for c in range(len(chests)):

                # Use c to get chest id
                chest = chests[c]

                # Create object and set position
                chestObject = annchienta.StaticObject( "chest", "locations/common/chest.xml" )

                chestObject.setPosition( annchienta.Point( annchienta.TilePoint, int(chest.getAttribute("tilex")), int(chest.getAttribute("tiley")) ) )

                # Create a unique id in the form of filename_layer_chestnr
                chestUniqueName = filename+"_"+str(i)+"_"+str(c)

                item = str( chest.getAttribute("item") )

                # Generate interact code
                code =  "import annchienta, PartyManager, SceneManager\n"
                code += "audioManager, cacheManager = annchienta.getAudioManager(), annchienta.getCacheManager()\n"
                code += "partyManager, sceneManager = PartyManager.getPartyManager(), SceneManager.getSceneManager()\n"
                code += "chest = annchienta.getPassiveObject()\n"
                code += "if not partyManager.hasRecord('"+chestUniqueName+"'):\n"
                code += " audioManager.playSound( cacheManager.getSound('sounds/chest.ogg') )\n"
                code += " chest.setAnimation( 'opened' )\n"
                code += " partyManager.inventory.addItem('"+item+"')\n"
                code += " partyManager.addRecord('"+chestUniqueName+"')\n"
                code += " sceneManager.text('Found "+item+".')\n"
                code += "else:\n"
                code += " sceneManager.text('This chest is empty!')\n"

                chestObject.setOnInteractCode( code )

                # Open chest if already opened
                if self.hasRecord( chestUniqueName ):
                    chestObject.setAnimation( "opened" )

                #print code

                # Add object to layer
                newMap.addObject( chestObject )

                # Make sure to keep a reference to avoid segmentation shit
                self.chestObjects += [chestObject]

        return newMap

    # Removes extra stuff from map.
    def freeMap( self, fMap ):

        # Remove chests from map
        while fMap.getObject( "chest" ):
            fMap.removeObject( fMap.getObject( "chest" ) )

    def changeMap( self, newMapFileName, newPosition = annchienta.Point(annchienta.TilePoint, 2, 2 ), newLayer = 0, fade=True ):

        if fade:
            self.sceneManager.fade()

        self.player.setPosition( newPosition )

        # Remove player from map
        self.currentMap.removeObject( self.player )

        self.lastMaps += [self.currentMap]
        self.currentMap = self.loadMap( newMapFileName )
        self.currentMap.setCurrentLayer( newLayer )
        self.currentMap.addObject( self.player )
        self.mapManager.setCurrentMap( self.currentMap )
        self.mapManager.cameraPeekAt( self.player, True )

        # Because loading a map can take some time:
        self.mapManager.resync()

    def changeLayer( self, index, newPosition = annchienta.Point( annchienta.TilePoint, 2, 2 ), fade = True ):

        if fade:
            self.sceneManager.fade()

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
        for combatant in self.team:
            combatant.setHp( combatant.getMaxHp() )
            combatant.setMp( combatant.getMaxMp() )

def init():
    global globalPartyManagerInstance
    globalPartyManagerInstance = PartyManager()

def getPartyManager():
    return globalPartyManagerInstance

