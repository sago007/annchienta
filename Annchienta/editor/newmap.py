from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import os
import annchienta
import pytileset
import mapfile

class NewMapDialog(QDialog):

    def __init__(self, editor):

        self.editor = editor

        # Init this widget
        QDialog.__init__(self, editor)
        uic.loadUi( "newmap.ui", self)

        self.connect( self.tilesetButton, SIGNAL("clicked()"), self.tilesetBrowse )
        self.connect( self.createButton, SIGNAL("clicked()"), self.createMap )

    def run(self):

        self.setModal(True)
        self.show()
        self.createButton.setEnabled(False)

    def createMap(self):
        tmap = annchienta.Map( int(self.widthBox.value()), int(self.heightBox.value()), str(self.tilesetDisplay.text()) )
        self.editor.currentMap = tmap
        self.editor.mapManager.setCurrentMap( tmap )
        self.editor.hasOpenedMap = True
        tmap.depthSort()
        self.accept()
        self.editor.tileset = pytileset.PyTileSet( self.editor, self.editor.currentMap.getTileSet().getDirectory() )
        self.editor.mapFile = mapfile.MapFile( self.editor )
        self.editor.mapFile.filename = "untitled"

    def tilesetBrowse(self):
        fileDialog = QFileDialog(self)
        filename = fileDialog.getExistingDirectory(self)
        self.tilesetDisplay.setText( filename )
        self.createButton.setEnabled(True)
