import annchienta
import xml.dom.minidom
import os

## A class that can write a map to a file
#
class MapWriter:

    ## Constructs a new MapWriter. When a filename
    #  is given, alter the file. With no filename,
    #  create a new document.
    def __init__( self, currentMap, fileName=None ):

        # Store the map and filename
        self.currentMap = currentMap
        self.fileName = fileName

        # Get a reference to the MapManager
        self.mapManager = annchienta.getMapManager()

        # Load the document if we specified a filename.
        # Else, create a new document.
        if fileName:

            self.document = xml.dom.minidom.parse( fileName )
            self.mapElement = self.document.getElementsByTagName("map")[0]

        else:

            self.document = xml.dom.minidom.Document()
            self.mapElement = self.document.createElement("map")
            
            # Set map attributes
            self.mapElement.setAttribute( "width", str( self.currentMap.getWidth() ) )
            self.mapElement.setAttribute( "height", str( self.currentMap.getHeight() ) )
            self.mapElement.setAttribute( "tilewidth", str( self.mapManager.getTileWidth() ) )
            self.mapElement.setAttribute( "tileheight", str( self.mapManager.getTileHeight() ) )
            self.mapElement.setAttribute( "tileset", str( self.toRelativePath( self.currentMap.getTileSet().getDirectory() ) ) )

            # Add to document
            self.document.appendChild( self.mapElement )

        # Now, we have the document in self.document and
        # the root element in self.mapElement.
        print self.document.toxml()

    def toRelativePath( self, target, base=os.curdir ):

        if not os.path.exists(target):
            raise OSError, 'Target does not exist: '+target
        if not os.path.isdir(base):
            raise OSError, 'Base is not a directory or does not exist: '+base

        base_list = (os.path.abspath(base)).split(os.sep)
        target_list = (os.path.abspath(target)).split(os.sep)

        if os.name in ['nt','dos','os2'] and base_list[0] <> target_list[0]:
            raise OSError, 'Target is on a different drive to base. Target: '+target_list[0].upper()+', base: '+base_list[0].upper()

        for i in range(min(len(base_list), len(target_list))):
            if base_list[i] != target_list[i]:
                break
            else:
                i+=1

        rel_list = [os.pardir] * (len(base_list)-i) + target_list[i:]
        return os.path.join(rel_list)

