from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import annchienta
import newmap
import tiles
import os
import pytileset
import mapfile

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
        self.engine = annchienta.getEngine()

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
        self.connect( self.refreshMapButton, SIGNAL("clicked()"), self.refreshMap )

        self.connect( self.saveMapButton, SIGNAL("clicked()"), self.saveMap )
        self.connect( self.saveMapAsButton, SIGNAL("clicked()"), self.saveMapAs )

        self.connect( self.tileWidthBox, SIGNAL("valueChanged(int)"), self.changeTileWidth )
        self.changeTileWidth()

        self.connect( self.addLayerButton, SIGNAL("clicked()"), self.addLayer )

        self.connect( self.nextLayerButton, SIGNAL("clicked()"), self.nextLayer )
        self.connect( self.layerZBox, SIGNAL("valueChanged(int)"), self.changeLayerZ )
        self.connect( self.layerOpacityBox, SIGNAL("valueChanged(int)"), self.changeLayerOpacity )

        #self.connect( self.zGroupBox, SIGNAL("toggled(bool)"), self.selectZGroupBox )
        #self.connect( self.tileGroupBox, SIGNAL("toggled(bool)"), self.selectTileGroupBox )
        #self.connect( self.tileSideGroupBox, SIGNAL("toggled(bool)"), self.selectTileSideGroupBox )

        self.connect( self.pythonClearButton, SIGNAL("clicked()"), self.clearPythonCode )
        self.connect( self.pythonExecuteButton, SIGNAL("clicked()"), self.executePythonCode )
        self.clearPythonCode()

        self.newMapDialog = newmap.NewMapDialog(self)

        self.selected = tiles.Selection()

    def selectGameDirectory(self):

        # Select a directory and set working directory
        fileDialog = QFileDialog(self)
        fileDialog.setDirectory(QString("../"))
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

        mpoint = annchienta.Point( annchienta.ScreenPoint, self.mouseX, self.mouseY )
        if self.hasOpenedMap:
            mpoint.y += self.currentMap.getCurrentLayer().getZ()
        mpoint.convert( annchienta.IsometricPoint )
        string = "Mouse: "+str(mpoint.x)+", "+str(mpoint.y)+" (iso) "
        mpoint.convert( annchienta.TilePoint )
        string += str(mpoint.x)+", "+str(mpoint.y)+" (tile)"
        self.mousePositionLabel.setText( QString( string ) )

        # NEVER Update the MapManager
        # LEAVE THIS COMMENTED
        # self.mapManager.update()

        # Draw
        self.videoManager.clear()
        if self.hasOpenedMap:
            self.mapManager.renderFrame()
            if bool(self.gridBox.isChecked()):
                self.drawGrid()
        self.videoManager.flip()

        if self.hasOpenedMap:
            self.currentMap.depthSort()
            self.selectAndApply()
            l = self.currentMap.getCurrentLayer()
            for o in range(l.getNumberOfObjects()):
                l.getObject(o).calculateCollidingTiles()
                l.getObject(o).calculateZFromCollidingTiles()

    # Creates a new map.
    def newMap(self):

        self.newMapDialog.run()

    # Opens and loads a map.
    def openMap(self):

        fileDialog = QFileDialog(self)
        filename = str(fileDialog.getOpenFileName(self))
        if not os.path.isfile(filename):
            return
        self.currentMap = annchienta.Map( filename )
        self.mapManager.setCurrentMap( self.currentMap )
        self.currentMap.depthSort()
        self.hasOpenedMap = True
        self.tileset = pytileset.PyTileSet( self, self.currentMap.getTileSet().getDirectory() )
        self.mapFile = mapfile.MapFile( self, filename )
        self.mapFile.filename = filename
        self.saveMapButton.setEnabled(True)
        self.engine.setWindowTitle( filename )

    # Opens and loads a map.
    def refreshMap(self):

        self.currentMap = annchienta.Map( self.mapFile.filename )
        self.mapManager.setCurrentMap( self.currentMap )
        self.currentMap.depthSort()
        self.tileset = pytileset.PyTileSet( self, self.currentMap.getTileSet().getDirectory() )
        self.mapFile = mapfile.MapFile( self, self.mapFile.filename )

    def saveMap(self):

        if self.hasOpenedMap:
            self.mapFile.write()

    def saveMapAs(self):

        fileDialog = QFileDialog(self)
        filename = str(fileDialog.getSaveFileName(self))
        self.mapFile.filename = os.path.abspath(filename)
        self.saveMapButton.setEnabled(True)
        if self.hasOpenedMap:
            self.mapFile.write()
        self.engine.setWindowTitle( filename )

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

        if bool(self.obstructionGroupBox.isChecked()):
            for y in range( 0, layer.getHeight() ):
                for x in range( 0, layer.getWidth() ):
                    tile = layer.getTile( x, y )
                    if tile.getObstructionType() == annchienta.DefaultObstruction:
                        self.videoManager.setColor( 0, 0, 0, 0 )
                    if tile.getObstructionType() == annchienta.NoObstruction:
                        self.videoManager.setColor( 0, 255, 0, 100 )
                    if tile.getObstructionType() == annchienta.FullObstruction:
                        self.videoManager.setColor( 255, 0, 0, 100 )

                    p = map( lambda i: tile.getPointPointer(i).to( annchienta.MapPoint ), range(4) )
                    self.videoManager.drawQuad( p[0].x, p[0].y, p[1].x, p[1].y, p[2].x, p[2].y, p[3].x, p[3].y )

        self.videoManager.setColor()

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

        if self.inputManager.buttonDown( 0 ):
            if bool(self.wholeTiles.isChecked()):
                for y in range( 0, layer.getHeight() ):
                    for x in range( 0, layer.getWidth() ):
                        tile = layer.getTile( x, y )
                        if tile.hasPoint( mouse ):
                            self.selected.tiles.append( tiles.AffectedTile( tile, True, True, True, True ) )
                            needsRecompiling = True
            else:
                # Move the mouse a little
                mouse.convert( annchienta.ScreenPoint )
                #mouse.x -= self.mapManager.getTileWidth()/4
                mouse.y += self.mapManager.getTileHeight()/2
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
                for y in range( gridh-1 ):
                    for x in range( gridw-1 ):
                        if mouse.isEnclosedBy( grid[ (y)*gridw+(x) ], grid[ (y+1)*gridw+(x+1) ] ):
                            if x-1 in range(layer.getWidth()) and y-1 in range(layer.getHeight()):
                                self.selected.tiles.append( tiles.AffectedTile( layer.getTile(x-1,y-1), False, False, True, False ) )
                            if x in range(layer.getWidth()) and y-1 in range(layer.getHeight()):
                                self.selected.tiles.append( tiles.AffectedTile( layer.getTile(x,y-1), False, True, False, False ) )
                            if x-1 in range(layer.getWidth()) and y in range(layer.getHeight()):
                                self.selected.tiles.append( tiles.AffectedTile( layer.getTile(x-1,y), False, False, False, True ) )
                            if x in range(layer.getWidth()) and y in range(layer.getHeight()):
                                self.selected.tiles.append( tiles.AffectedTile( layer.getTile(x,y), True, False, False, False ) )
                            needsRecompiling = True


        # APPLY PART

        if bool(self.zGroupBox.isChecked()):
            for at in self.selected.tiles:
                for p in at.points:
                    at.tile.setZ( p, int(self.tileZBox.value()) )

        if bool(self.tileGroupBox.isChecked()):
            for at in self.selected.tiles:
                for p in at.points:
                    at.tile.setSurface( p, self.tileset.selectedTile )

        if bool(self.tileSideGroupBox.isChecked()):
            for at in self.selected.tiles:
                at.tile.setSideSurface( self.tileset.selectedTileSide )
                at.tile.setSideSurfaceOffset( int(self.tileSideOffsetBox.value()) )

        if bool(self.obstructionGroupBox.isChecked()):
            for at in self.selected.tiles:
                at.tile.setObstructionType( int(self.obstructionTypeBox.currentIndex()) )

        for at in self.selected.tiles:
            at.tile.setShadowed( bool(self.shadowedBox.isChecked() ) )

        #if needsRecompiling:
        #    for at in self.selected.tiles:
        #        at.tile.makeList()

            # Does not work anyway
            #self.currentMap.update()

    def addLayer(self):

        if not self.hasOpenedMap:
            return
        self.currentMap.addNewLayer( int(self.addLayerZBox.value()) )
        self.currentMap.sortLayers()
        le = self.mapFile.document.createElement( "layer" )
        self.mapFile.mapElement.appendChild( le )

    def nextLayer(self):

        if not self.hasOpenedMap:
            return
        i = self.currentMap.getCurrentLayerIndex()
        i = (i+1)%self.currentMap.getNumberOfLayers()
        self.currentMap.setCurrentLayer(i)
        self.layerZBox.setValue( self.currentMap.getCurrentLayer().getZ() )
        self.layerOpacityBox.setValue( self.currentMap.getCurrentLayer().getOpacity() )

    def changeLayerZ(self):

        self.currentMap.getCurrentLayer().setZ( int(self.layerZBox.value()) )
        self.currentMap.sortLayers()
        
    def changeLayerOpacity(self):

        self.currentMap.getCurrentLayer().setOpacity( int(self.layerOpacityBox.value()) )
        
    def selectZGroupBox(self):
        if bool(self.zGroupBox.isChecked()):
            self.tileGroupBox.setChecked(False)
            self.tileSideGroupBox.setChecked(False)
        
    def selectTileGroupBox(self):
        if bool(self.tileGroupBox.isChecked()):
            self.zGroupBox.setChecked(False)
            self.tileSideGroupBox.setChecked(False)
            
    def selectTileSideGroupBox(self):
        if bool(self.tileSideGroupBox.isChecked()):
            self.zGroupBox.setChecked(False)
            self.tileGroupBox.setChecked(False)

    def clearPythonCode(self):
        self.pythonCode.setPlainText("import annchienta\n")

    def executePythonCode(self):
        code = str(self.pythonCode.toPlainText())
        exec( code )

