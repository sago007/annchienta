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

    def toRelativePath( self, dest, base=os.getcwd() ):

        # Normalize
        p1 = os.path.normpath( os.path.abspath( base ) )
        p2 = os.path.normpath( os.path.abspath( dest ) )

        # Split /a/b/c to ['a', 'b', 'c']
        l1 = p1.split( os.path.sep )
        l2 = p2.split( os.path.sep )

        # Remove equal start
        while len(l1) and len(l2) and l1[0]==l2[0]:
            l1 = l1[1:]
            l2 = l2[1:]

        # Add ../ and then the remaining part of l2
        path = '../'*len(l1)
        for remaining in l2:
            path += '/' + remaining

        return os.path.normpath( path )
