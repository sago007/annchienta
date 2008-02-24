from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import annchienta
import newmap
import selection
import os
import pytileset

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

        self.connect( self.tileWidthBox, SIGNAL("valueChanged(int)"), self.changeTileWidth )
        self.changeTileWidth()

        self.connect( self.addLayerButton, SIGNAL("clicked()"), self.addLayer )

        self.connect( self.nextLayerButton, SIGNAL("clicked()"), self.nextLayer )
        self.connect( self.layerZBox, SIGNAL("valueChanged(int)"), self.changeLayerZ )

        self.newMapDialog = newmap.NewMapDialog(self)

        self.selected = selection.Selection()

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
            if bool(self.gridBox.isChecked()):
                self.drawGrid()
        self.videoManager.end()

        if self.hasOpenedMap:
            self.selectAndApply()

    # Creates a new map.
    def newMap(self):

        self.newMapDialog.run()

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
        self.tileset = pytileset.PyTileSet( self, self.currentMap.getTileSet().getDirectory() )

    def drawGrid(self):

        self.videoManager.translate( -self.mapManager.getCameraX(), -self.mapManager.getCameraY() )
        self.videoManager.translate( 0, -self.currentMap.getCurrentLayer().getZ() )
        self.videoManager.setColor( 255, 255, 255, 200 )

        layer = self.currentMap.getCurrentLayer()
        for y in range( 1, layer.getHeight() ):
            point1 = layer.getTile( 0, y ).getPointPointer(0)
            point2 = layer.getTile( layer.getWidth()-1, y-1 ).getPointPointer(2)
            self.videoManager.drawLine( point1.x, point1.y, point2.x, point2.y )

        for x in range( 1, layer.getWidth() ):
            point1 = layer.getTile( x, 0 ).getPointPointer(0)
            point2 = layer.getTile( x-1, layer.getHeight()-1 ).getPointPointer(2)
            self.videoManager.drawLine( point1.x, point1.y, point2.x, point2.y )

    def changeTileWidth(self):

        self.tileHeightBox.setValue( int(self.tileWidthBox.value())/2 )
        self.mapManager.setTileWidth( int(self.tileWidthBox.value()) )
        self.mapManager.setTileHeight( int(self.tileHeightBox.value()) )

    def selectAndApply(self):

        needsRecompiling = False

        # SELECT PART

        self.selected.clear()

        layer = self.currentMap.getCurrentLayer()

        mouse = annchienta.Point( annchienta.ScreenPoint, self.inputManager.getMouseX(), self.inputManager.getMouseY() )
        mouse.y += self.currentMap.getCurrentLayer().getZ()

        if self.inputManager.buttonDown( 0 ) or (bool(self.zGroupBox.isChecked()) and self.inputManager.buttonTicked(0)):
            if bool(self.wholeTiles.isChecked()):
                for y in range( 0, layer.getHeight() ):
                    for x in range( 0, layer.getWidth() ):
                        tile = layer.getTile( x, y )
                        if tile.hasPoint( mouse ):
                            self.selected.tiles.append( selection.AffectedTile( tile, True, True, True, True ) )
                            needsRecompiling = True
            else:
                # Move the mouse a little
                mouse.convert( annchienta.ScreenPoint )
                #mouse.x -= self.mapManager.getTileWidth()/4
                mouse.y -= self.mapManager.getTileHeight()/2
                mouse.convert( annchienta.IsometricPoint )
                # Create a new pseudo-tilegrid
                grid = []
                gridh, gridw = layer.getHeight()+2, layer.getWidth()+2
                for y in range( 0, gridh ):
                    for x in range( 0, gridw ):
                        point = annchienta.Point( annchienta.TilePoint, x, y, 0 )
                        point.convert( annchienta.IsometricPoint )
                        grid.append( point )
                # Now check for collision
                for y in range( 1, gridh ):
                    for x in range( 1, gridw ):
                        if mouse.isEnclosedBy( grid[ (y-1)*gridw+(x-1) ], grid[ y*gridw+x ] ):
                            #print x, y
                            if x-1 in range(0,layer.getWidth()) and y-1 in range(0,layer.getHeight()):
                                self.selected.tiles.append( selection.AffectedTile( layer.getTile(x-1,y-1), False, False, True, False ) )
                            if x in range(0,layer.getWidth()) and y-1 in range(0,layer.getHeight()):
                                self.selected.tiles.append( selection.AffectedTile( layer.getTile(x,y-1), False, True, False, False ) )
                            if x-1 in range(0,layer.getWidth()) and y in range(0,layer.getHeight()):
                                self.selected.tiles.append( selection.AffectedTile( layer.getTile(x-1,y), False, False, False, True ) )
                            if x in range(0,layer.getWidth()) and y in range(0,layer.getHeight()):
                                self.selected.tiles.append( selection.AffectedTile( layer.getTile(x,y), True, False, False, False ) )
                            needsRecompiling = True

                print "Here."

        # APPLY PART

        if bool(self.zGroupBox.isChecked()) and self.inputManager.buttonTicked(0):
            for at in self.selected.tiles:
                for p in at.points:
                    point = at.tile.getPointPointer(p)
                    point.z = point.z + int(self.tileZBox.value())
                    #point.y = point.y - int(self.tileZBox.value())/2

        if bool(self.tileGroupBox.isChecked()):
            for at in self.selected.tiles:
                for p in at.points:
                    surface = self.currentMap.getTileSet().getSurface( self.tileset.selectedTile )
                    at.tile.setSurface( p, surface )

        if bool(self.tileSideGroupBox.isChecked()):
            for at in self.selected.tiles:
                surface = self.currentMap.getTileSet().getSideSurface( self.tileset.selectedTile )
                at.tile.setSideSurface( surface )

        if needsRecompiling:
            for at in self.selected.tiles:
                at.tile.makeList()

            # Does not work anyway
            #self.currentMap.update()

    def addLayer(self):

        if not self.hasOpenedMap:
            return
        self.currentMap.addNewLayer( int(self.addLayerZBox.value()) )
        self.currentMap.sortLayers()

    def nextLayer(self):

        if not self.hasOpenedMap:
            return
        i = self.currentMap.getCurrentLayerIndex()
        i = (i+1)%self.currentMap.getNumberOfLayers()
        self.currentMap.setCurrentLayer(i)
        self.layerZBox.setValue( self.currentMap.getCurrentLayer().getZ() )

    def changeLayerZ(self):

        self.currentMap.getCurrentLayer().setZ( int(self.layerZBox.value()) )
        self.currentMap.sortLayers()