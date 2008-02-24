from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

class SurfaceButton(QToolButton):

    def __init__(self, parent, surface, number, tileset):
        
        QToolButton.__init__(self, parent)
        self.setIcon( QIcon(surface) )
        self.setIconSize( QSize(surface.width(), surface.height()) )
        
        self.tileset = tileset
        self.number = number

        self.connect( self, SIGNAL("clicked()"), self.onSelected )

    def onSelected(self):
        self.tileset.selectedTile = self.number
        #print "Selected tile", self.number


class PyTileSet:

    def __init__( self, editor, directory ):

        self.editor = editor

        self.surfaces, self.sideSurfaces = [], []
        
        nullSurface = QPixmap(self.editor.mapManager.getTileWidth(), self.editor.mapManager.getTileHeight() )
        nullSurface.fill( QColor(0,0,0,0) )
        self.surfaces.append( nullSurface )
        self.sideSurfaces.append( nullSurface )

        searching = True
        i = 1
        while searching:
            fn = directory+"/"+str(i)+".png"
            if os.path.isfile(fn):
                self.surfaces.append( QPixmap(fn) )
                i+=1
            else:
                searching = False

        searching = True
        i = 1
        while searching:
            fn = directory+"/side"+str(i)+".png"
            if os.path.isfile(fn):
                self.sideSurfaces.append( QPixmap(fn) )
                i+=1
            else:
                searching = False

        self.editor.connect( self.editor.showTileSurfacesButton, SIGNAL("clicked()"), self.showSurfaces )
        self.editor.connect( self.editor.showTileSideSurfacesButton, SIGNAL("clicked()"), self.showSideSurfaces )

        self.selectedTile = 0

    def showSurfaces(self):
        self.show( self.surfaces )

    def showSideSurfaces(self):
        self.show( self.sideSurfaces )
        
    def show(self, array):
        
        self.scrollArea = QScrollArea()
        
        self.scrollArea.setWindowTitle("Tile Selector")

        self.mainWidget = QWidget(self.scrollArea)
        self.grid = QGridLayout(self.scrollArea)
        self.mainWidget.setLayout( self.grid )
        
        for i in range(0,len(array)):
            button = SurfaceButton( self.mainWidget, array[i], i, self )
            self.grid.addWidget( button, i/3, i%3 )

        self.scrollArea.setWidget( self.mainWidget )
        self.scrollArea.setMaximumWidth(400)

        self.scrollArea.show()
