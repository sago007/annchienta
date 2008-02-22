from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import annchienta
import newmap
import os

class Editor(QWidget):

    def __init__(self):

        # Init this widget
        QWidget.__init__(self)
        uic.loadUi("editor.ui", self)

        self.hasOpenedMap = False

        # Create an annchienta context
        self.videoManager = annchienta.getVideoManager()
        self.mapManager = annchienta.getMapManager()
        self.inputManager = annchienta.getInputManager()

        # Set the video mode
        self.videoManager.setVideoMode( 600, 500, "Map", False )

        # Mouse
        self.mouseX, self.mouseY = 0, 0

        # Create a timer that will update the map from time to time.
        self.timer = QTimer(self)
        self.connect( self.timer, SIGNAL("timeout()"), self.updateMap )
        self.timer.start(60)

        # Connect configuration buttons
        self.connect( self.selectGameDirectoryButton, SIGNAL("clicked()"), self.selectGameDirectory )

        # Connect map buttons
        self.connect( self.newMapButton, SIGNAL("clicked()"), self.newMap )
        self.connect( self.openMapButton, SIGNAL("clicked()"), self.openMap )

        self.newMapDialog = newmap.NewMapDialog(self)

    def selectGameDirectory(self):

        # Select a directory and set working directory
        fileDialog = QFileDialog(self)
        filename = fileDialog.getExistingDirectory(self)
        # Set lineEdit to match
        self.selectGameDirectoryDisplay.setText( filename )
        os.chdir( str(filename) )

    # Gets automatically called every {whaterver} milliseconds.
    def updateMap(self):

        # Update the InputManager
        self.inputManager.update()
        if not self.inputManager.running():
            self.close()

        # Drag the map with the mouse
        if self.inputManager.buttonDown(1):
            cx, cy = self.mapManager.getCameraX(), self.mapManager.getCameraY()
            self.mapManager.setCameraX( cx + self.mouseX - self.inputManager.getMouseX() )
            self.mapManager.setCameraY( cy + self.mouseY - self.inputManager.getMouseY() )

        self.mouseX, self.mouseY = self.inputManager.getMouseX(), self.inputManager.getMouseY()

        # NEVER Update the MapManager
        # LEAVE THIS COMMENTED
        # self.mapManager.update()

        # Draw
        self.videoManager.begin()
        if self.hasOpenedMap:
            self.mapManager.renderFrame()
            self.drawGrid()
        self.videoManager.end()

    # Creates a new map.
    def newMap(self):

        self.newMapDialog.run()
        self.hasOpenedMap = True

    # Opens and loads a map.
    def openMap(self):

        fileDialog = QFileDialog(self)
        filename = fileDialog.getOpenFileName(self)
        if not os.path.isfile(filename):
            return
        self.currentMap = annchienta.Map( str(filename) )
        self.mapManager.setCurrentMap( self.currentMap )
        self.currentMap.depthSort()
        self.hasOpenedMap = True

    def drawGrid(self):

        self.videoManager.translate( -self.mapManager.getCameraX(), -self.mapManager.getCameraY() )
        self.videoManager.setColor( 255, 0, 0, 100 )

        layer = self.currentMap.getCurrentLayer()
        for y in range( 1, layer.getHeight() ):
            point1 = layer.getTile( 0, y ).getPointPointer(0)
            point2 = layer.getTile( layer.getWidth()-1, y-1 ).getPointPointer(2)
            self.videoManager.drawLine( point1.x, point1.y, point2.x, point2.y )

        for x in range( 1, layer.getWidth() ):
            point1 = layer.getTile( x, 0 ).getPointPointer(0)
            point2 = layer.getTile( x-1, layer.getHeight()-1 ).getPointPointer(2)
            self.videoManager.drawLine( point1.x, point1.y, point2.x, point2.y )
