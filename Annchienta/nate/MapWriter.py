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

            # Temporary filename
            fileName = "untitled.xml"

        # Now, we have the document in self.document and
        # the root element in self.mapElement.

    ## Saves the map to the filename that should already be set.
    #  This basically detects changes in the map and writes those
    #  to the xml file.
    def saveMap( self ):

        layerElements = self.document.getElementsByTagName("layer")

        # Update the number of layers in the map file
        while self.currentMap.getNumberOfLayers() > len(layerElements):
            newLayerElement = self.document.createElement("layer")
            self.mapElement.appendChile( newLayerElement )

        # Now get the again
        layerElements = self.document.getElementsByTagName("layer")

        # Now go through all layers
        for l in range( len( layerElements ) ):

            layer = self.currentMap.getLayer(l)
            layerElement = layerElements[l]

            # Update Z
            layerElement.setAttribute( "z", str(layer.getZ()) )

            # Get the tiles element
            tileElements = layerElement.getElementsByTagName("tiles")
            # Add one if there is none
            if not len(tileElements):
                tileElements = [ self.document.createElement("tiles") ]
                layerElement.appendChild( tileElements[0] )
            tileElement = tileElements[0]

            # Remove all the children of the tile element, we want to
            # fill it with our own tiles.
            while tileElement.hasChildNodes():
                tileElement.removeChild( tileElement.lastChild )

            # Now start filling in the text data
            data = "\n"

            # Loop through all tiles, appending them to data
            for y in range(layer.getHeight()):
                data += "    "
                for x in range(layer.getWidth()):
                    tile = layer.getTile(x,y)
                    for i in range(4):
                        data += (str(tile.getPointPointer(i).z)+" "+str(tile.getSurface(i))+" ")
                    data += (str(tile.getSideSurfaceOffset())+" ")
                    data += (str(tile.getSideSurface())+"    ")
                data += "\n"

            # Now add the data as a child node.
            dataNode = self.document.createTextNode( data )
            tileElement.appendChild( dataNode )

            # Collect obstruction values
            obstructions = []
            for y in range(layer.getHeight()):
                for x in range(layer.getWidth()):
                    obstructions.append( layer.getTile(x,y).getObstructionType() )

            # write only if there are non-default values.
            if len( filter( lambda o: o!=annchienta.DefaultObstruction, obstructions ) ):

                # Get the obstruction element, or create one if there
                # isn't any present.
                obstructionElements = layerElement.getElementsByTagName("obstruction")
                if not len(obstructionElements):
                    obstructionElements = [ self.document.createElement("obstruction") ]
                    layerElement.appendChild( obstructionElements[0] )
                obstructionElement = obstructionElements[0]

                # Remove all children, we want to redefine it
                while obstructionElement.hasChildNodes():
                    obstructionElement.removeChild( obstructionElement.lastChild )

                # Write all obstruction codes to data
                data = "\n    "
                for i in obstructions:
                    data += str(i) + " "
                data += "\n"

                # Append that data to the obstruction node
                dataNode = self.document.createTextNode( data )
                obstructionElement.appendChild( dataNode )

            # In case there are only default obstruction values,
            # storing them would be quite a waste. So remove the
            # entire obstruction node.
            else:
                obstructionElements = layerElements[l].getElementsByTagName("obstruction")
                for o in obstructionElements:
                    layerElements[l].removeChild(o)

            # Get all shadowed values
            shadowed = []
            for y in range(layer.getHeight()):
                for x in range(layer.getWidth()):
                    shadowed.append( layer.getTile(x,y).isShadowed() )

            # If there any shadowed tiles, we have to write them
            if len( filter( lambda s: s, shadowed ) ):

                # Retrieve the shadowed elements
                shadowedElements = layerElements[l].getElementsByTagName("shadowed")
                if not len(shadowedElements):
                    shadowedElements = [ self.document.createElement("shadowed") ]
                    layerElement.appendChild( shadowedElements[0] )
                shadowedElement = shadowedElements[0]

                # remove all children
                while shadowedElement.hasChildNodes():
                    shadowedElement.removeChild( shadowedElement.lastChild )

                # Write the shadowed values to data
                data = "\n    "
                for i in shadowed:
                    data += str(int(i)) + " "
                data += "\n"

                # Append the data to the shadowed node
                dataNode = self.document.createTextNode( data )
                shadowedElement.appendChild( dataNode )

            # If there are no shadowed tiles at all, just remove
            # the shadowed element.
            else:
                shadowedElements = layerElements[l].getElementsByTagName("shadowed")
                for s in shadowedElements:
                    layerElements[l].removeChild(s)


        # End by writing everything to the file
        file = open( self.fileName, 'w' )
        file.write( self.document.toxml() )
        file.close()

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
