import annchienta

def writeMap( editor, filename ):
    
    f = open(filename, "w")
    
    for l in range(editor.currentMap.getNumberOfLayers()):

        f.write("    <layer>\n        <tiles>\n")

        layer = editor.currentMap.getLayer(l)
        for y in range(layer.getHeight()):
            f.write("            ")
            for x in range(layer.getWidth()):
                tile = layer.getTile(x,y)
                for i in range(4):
                    f.write( str(tile.getPointPointer(i).z)+" "+str(tile.getSurface(i))+" " )
                f.write( str(tile.getSideSurface())+"    " )
            f.write("\n")

        f.write("        </tiles>\n    </layer>\n")

    f.close()
