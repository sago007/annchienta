import annchienta
import xml.dom.minidom
from Chest import Chest
import PartyManager

class MapLoader(object):

    def __init__( self ):
        pass

    def loadMap( self, fileName ):

        partyManager = PartyManager.getPartyManager()

        # Load the map though annchienta
        loadedMap = annchienta.Map( fileName )
        # Get the actual xml
        document = xml.dom.minidom.parse( fileName )

        layers = document.getElementsByTagName( "layer" )
        for i in range(len(layers)):

            loadedMap.setCurrentLayer( i )
            chestElements = layers[i].getElementsByTagName( "chest" )

            for c in range(len(chestElements)):

                # Create a unique id in the form of filename_layer_chestnr
                uniqueId = fileName + "_" + str(i) + "_" + str(c)
                item = str( chestElements[c].getAttribute("item") )
                chest = Chest( item, uniqueId )

                if partyManager.hasRecord( uniqueId ):
                    chest.setAnimation( "opened" )

                loadedMap.addObject( chest, annchienta.Point( annchienta.TilePoint, int(chestElements[c].getAttribute("tilex")), int(chestElements[c].getAttribute("tiley")) ) )
                # Do not keep this reference
                chest = chest.__disown__()

        return loadedMap
