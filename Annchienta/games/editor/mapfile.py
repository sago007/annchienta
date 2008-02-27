import annchienta
import xml.dom.ext
import xml.dom.minidom
import os

def relpath(target, base=os.curdir):

    if not os.path.exists(target):
        raise OSError, 'Target does not exist: '+target
    if not os.path.isdir(base):
        raise OSError, 'Base is not a directory or does not exist: '+base

    base_list = (os.path.abspath(base)).split(os.sep)
    target_list = (os.path.abspath(target)).split(os.sep)

    if os.name in ['nt','dos','os2'] and base_list[0] <> target_list[0]:
        raise OSError, 'Target is on a different drive to base. Target: '+target_list[0].upper()+', base: '+base_list[0].upper()

    for i in range(min(len(base_list), len(target_list))):
        if base_list[i] <> target_list[i]: break
    else:
        i+=1

    rel_list = [os.pardir] * (len(base_list)-i) + target_list[i:]
    return os.path.join(*rel_list)

class MapFile:

    def __init__( self, editor, filename="untitled" ):

        self.editor = editor

        self.filename = filename
        if filename=="untitled":
            self.document = xml.dom.minidom.Document()
            self.mapElement = self.document.createElement("map")
            self.mapElement.setAttribute("width", str(editor.currentMap.getWidth()) )
            self.mapElement.setAttribute("height", str(editor.currentMap.getWidth()) )
            self.mapElement.setAttribute("tilewidth", str(editor.mapManager.getTileWidth() ) )
            self.mapElement.setAttribute("tileheight", str(editor.mapManager.getTileHeight() ) )
            self.mapElement.setAttribute("tileset", relpath( os.path.abspath(editor.currentMap.getTileSet().getDirectory() ), str(editor.selectGameDirectoryDisplay.text()) ))
            self.document.appendChild( self.mapElement )

        else:
            self.document = xml.dom.minidom.parse( self.filename )
            self.mapElement = self.document.getElementsByTagName("map")[0]

    def write( self ):
        self.update()
        file = open( self.filename, "wb" )
        xml.dom.ext.PrettyPrint( self.document, file )
        file.close()

    def update( self ):

        layerElements = self.document.getElementsByTagName("layer")
        if not len(layerElements):
            layerElements = [ self.document.createElement("layer") ]
            self.mapElement.appendChild( layerElements[0] )

        for l in range(len(layerElements)):

            layer = self.editor.currentMap.getLayer(l)
            layerElements[l].setAttribute( "z", str(layer.getZ()) )

            tileElements = layerElements[l].getElementsByTagName("tiles")
            if not len(tileElements):
                tileElements = [ self.document.createElement("tiles") ]
                layerElements[l].appendChild( tileElements[0] )

            # remove all children
            while tileElements[0].hasChildNodes():
                tileElements[0].removeChild( tileElements[0].lastChild )

            data = ""

            for y in range(layer.getHeight()):
               for x in range(layer.getWidth()):
                    tile = layer.getTile(x,y)
                    for i in range(4):
                        data += (str(tile.getPointPointer(i).z)+" "+str(tile.getSurface(i))+" ")
                    data += (str(tile.getSideSurface())+"    ")
               data += "\n"

            dataNode = self.document.createTextNode( data )
            tileElements[0].appendChild( dataNode )
