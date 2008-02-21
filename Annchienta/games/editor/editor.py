from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import annchienta

class Editor(QWidget):

    def __init__(self):

        # Init this widget
        QWidget.__init__(self)
        uic.loadUi("editor.ui", self)

        # Create an annchienta context
        self.videoManager = annchienta.getVideoManager()
        self.mapManager = annchienta.getMapManager()
        self.inputManager = annchienta.getInputManager()

        # Set the video mode
        self.videoManager.setVideoMode( 600, 500, "Map", False )

        # Create a timer that will update the map from time to time.
        self.timer = QTimer(self)
        #self.connect( self.timer, SIGNAL("timeout()"), self, SLOT("update()"))
        self.connect( self.timer, SIGNAL("timeout()"), self.updateMap )
        self.timer.start(100)

    # Gets automatically called every {whaterver} milliseconds.
    def updateMap(self):

        # Update the InputManager
        self.inputManager.update()
        if not self.inputManager.running():
            self.close()

        # NEVER Update the MapManager
        # LEAVE THIS COMMENTED
        # self.mapManager.update()

        # Draw
        self.videoManager.begin()
        self.mapManager.renderFrame()
        self.videoManager.end()

    #self.connect(self.openButton, SIGNAL("clicked()"), self.open)
    #self.connect(self.saveButton, SIGNAL("clicked()"), self.save)
