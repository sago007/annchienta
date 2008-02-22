from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import os
import annchienta

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

    def createMap(self):
        tmap = annchienta.Map( int(self.widthBox.value()), int(self.heightBox.value()), str(self.tilesetDisplay.text()) )
        self.editor.currentMap = tmap
        self.editor.mapManager.setCurrentMap( tmap )
        self.editor.hasOpenedMap = True
        tmap.depthSort()
        self.accept()

    def tilesetBrowse(self):
        fileDialog = QFileDialog(self)
        filename = fileDialog.getExistingDirectory(self)
        self.tilesetDisplay.setText( filename )
