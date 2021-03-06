/*  This file is part of Annchienta.
 *  Copyright 2008 (C) Jasper Van der Jeugt
 *
 *  Annchienta is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Annchienta is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with Annchienta.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "Map.h"

#include <SDL_opengl.h>
#include <sstream>
#include <vector>
#include <Python.h>
#include "xml/irrXML.h"
using namespace irr;
using namespace io;
#include "Tile.h"
#include "TileSet.h"
#include "Entity.h"
#include "Layer.h"
#include "MapManager.h"
#include "StaticObject.h"
#include "Person.h"
#include "Point.h"
#include "Area.h"
#include "Engine.h"
#include "CacheManager.h"
#include "LogManager.h"
#include "InputManager.h"
#include "VideoManager.h"

namespace Annchienta
{

    Map::Map( const char *_fileName, bool scripts ): sortedLayers(0), currentLayer(0), onPreRenderCode(0), onPreRenderScript(0),
                                                     onPostRenderCode(0), onPostRenderScript(0)
    {
        Engine *engine = getEngine();
        LogManager *logManager = getLogManager();
        CacheManager *cacheManager = getCacheManager();
        videoManager = getVideoManager();

        Layer *layer = 0;

        if( !engine->isValidFile(_fileName) )
            logManager->error( "'%s' is not a valid file.", _fileName );

        IrrXMLReader *xml = createIrrXMLReader( _fileName );

        strcpy( fileName, _fileName );

        if( !xml )
            logManager->error( "Could not open given map file '%s' as xml.", _fileName );

        /** Read through the entire xml file. */
        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    if( !strcmp("map", xml->getNodeName()) )
                    {
                        if( xml->getAttributeValue("width") && xml->getAttributeValue("height") )
                        {
                            width = xml->getAttributeValueAsInt("width");
                            height = xml->getAttributeValueAsInt("height");
                        }
                        else
                            logManager->warning( "'%s' does not provide map width and height.", fileName);

                        if( xml->getAttributeValue("tilewidth") && xml->getAttributeValue("tileheight") )
                        {
                            getMapManager()->setTileWidth( xml->getAttributeValueAsInt("tilewidth") );
                            getMapManager()->setTileHeight( xml->getAttributeValueAsInt("tileheight") );
                        }
                        else
                            logManager->warning("'%s' does not provide tilewidth and tileheight.", fileName);

                        if( xml->getAttributeValue("tileset") )
                            tileSet = new TileSet( xml->getAttributeValue("tileset") );
                        else
                            logManager->warning("'%s' does not provide a valid tileset.", fileName);
                    }
                    if( !strcmp("layer", xml->getNodeName()) )
                    {
                        int opacity = xml->getAttributeValue("opacity") ? xml->getAttributeValueAsInt("opacity"):0xff,
                            z = xml->getAttributeValue("z") ? xml->getAttributeValueAsInt("z"):0;

                        layer = new Layer( tileSet, width, height, opacity, z );
                    }
                    if( !strcmp("tiles", xml->getNodeName()) )
                    {
                        /* Read to the node and get the (text) data from it. */
                        xml->read();
                        std::stringstream data( xml->getNodeData() );

                        /* Allocate some room for the tiles. */
                        Tile **tiles = new Tile*[width*height];

                        for( int y=0; y<height; y++ )
                        {
                            for( int x=0; x<width; x++ )
                            {
                                Point points[4];
                                int surfaces[4];
                                int sideSurfaceOffset;
                                int sideSurface;

                                /* Simply use tile coordinates. */
                                points[0].y = points[3].y = y;
                                points[1].y = points[2].y = y+1;
                                points[0].x = points[1].x = x;
                                points[2].x = points[3].x = x+1;

                                for( int p=0; p<4; p++ )
                                {
                                    points[p].setType( TilePoint );
                                    data >> points[p].z;
                                    data >> surfaces[p];
                                }

                                data >> sideSurfaceOffset;
                                data >> sideSurface;

                                tiles[y*width+x] = new Tile( tileSet, points[0], surfaces[0],
                                                             points[1], surfaces[1],
                                                             points[2], surfaces[2],
                                                             points[3], surfaces[3],
                                                             sideSurfaceOffset, sideSurface );

                            }
                        }

                        layer->setTiles( tiles );
                    }
                    if( !strcmp("obstruction", xml->getNodeName()) )
                    {
                        xml->read();
                        if( layer->hasTiles() )
                        {
                            std::stringstream data( xml->getNodeData() );
                            for( int y=0; y<height; y++ )
                            {
                                for( int x=0; x<width; x++ )
                                {
                                    int obstruction;
                                    data >> obstruction;
                                    layer->getTile(x,y)->setObstructionType( (ObstructionType) obstruction );
                                }
                            }
                        }
                        else
                        {
                            logManager->warning("Obstruction defined before tile data in '%s'. Ignoring.", fileName);
                        }
                        xml->read();
                    }
                    if( !strcmp("shadowed", xml->getNodeName()) )
                    {
                        xml->read();
                        if( layer->hasTiles() )
                        {
                            std::stringstream data( xml->getNodeData() );
                            for( int y=0; y<height; y++ )
                            {
                                for( int x=0; x<width; x++ )
                                {
                                    int shadowed;
                                    data >> shadowed;
                                    layer->getTile(x,y)->setShadowed( (bool) shadowed );
                                }
                            }
                        }
                        else
                        {
                            logManager->warning("Shadow properties defined before tile data in '%s'. Ignoring.", fileName);
                        }
                        xml->read();
                    }
                    if( !strcmp("staticobject", xml->getNodeName() ) )
                    {
                        StaticObject *staticObject;

                        if( xml->getAttributeValue("config") )
                            staticObject = new StaticObject( xml->getAttributeValue("name"), xml->getAttributeValue("config") );
                        else
                        {
                            /* StaticObjects don't *NEED* a config file.
                             */
                            Surface *s = cacheManager->getSurface( xml->getAttributeValue("sprite") );
                            Mask *m = cacheManager->getMask( xml->getAttributeValue("mask") );
                            staticObject = new StaticObject( xml->getAttributeValue("name"), s, m );
                        }

                        Point position;

                        if( xml->getAttributeValue("isox") && xml->getAttributeValue("isoy") )
                            position = Point( IsometricPoint, xml->getAttributeValueAsInt("isox"),
                                              xml->getAttributeValueAsInt("isoy"), 0 );

                        if( xml->getAttributeValue("mapx") && xml->getAttributeValue("mapy") )
                            position = Point( MapPoint, xml->getAttributeValueAsInt("mapx"),
                                              xml->getAttributeValueAsInt("mapy"), 0 );

                        if( xml->getAttributeValue("tilex") && xml->getAttributeValue("tiley") )
                            position = Point( TilePoint, xml->getAttributeValueAsInt("tilex"),
                                              xml->getAttributeValueAsInt("tiley"), 0 );

                        if( xml->getAttributeValueAsInt("camera") )
                            getMapManager()->cameraFollow( staticObject );

                        if( xml->getAttributeValue("animation") )
                            staticObject->setAnimation( xml->getAttributeValue("animation") );

                        layer->addObject( staticObject, position );

                    }
                    if( !strcmp("person", xml->getNodeName() ) )
                    {
                        Person *person;
                        Point position;

                        if( xml->getAttributeValue("name") && xml->getAttributeValue("config") )
                            person = new Person( xml->getAttributeValue("name"), xml->getAttributeValue("config") );
                        else
                            logManager->error("No name and config specified for person in %s.", fileName);

                        if( xml->getAttributeValue("isox") && xml->getAttributeValue("isoy") )
                            position = Point( IsometricPoint, xml->getAttributeValueAsInt("isox"),
                                              xml->getAttributeValueAsInt("isoy"), 0 );

                        if( xml->getAttributeValue("mapx") && xml->getAttributeValue("mapy") )
                            position = Point( MapPoint, xml->getAttributeValueAsInt("mapx"),
                                              xml->getAttributeValueAsInt("mapy"), 0 );

                        if( xml->getAttributeValue("tilex") && xml->getAttributeValue("tiley") )
                            position = Point( TilePoint, xml->getAttributeValueAsInt("tilex"),
                                              xml->getAttributeValueAsInt("tiley"), 0 );

                        if( xml->getAttributeValueAsInt("camera") )
                            getMapManager()->cameraFollow( person);

                        if( xml->getAttributeValue("animation") )
                            person->setAnimation( xml->getAttributeValue("animation") );

                        layer->addObject( person, position );

                    }
                    if( !strcmp("area", xml->getNodeName() ) )
                    {
                        Point p1, p2;
                        bool visible = false;

                        if( xml->getAttributeValue("isox1") )
                        {
                            p1 = Point( IsometricPoint, xml->getAttributeValueAsInt("isox1"), xml->getAttributeValueAsInt("isoy1"), 0 );
                            p2 = Point( IsometricPoint, xml->getAttributeValueAsInt("isox2"), xml->getAttributeValueAsInt("isoy2"), 0 );
                        }
                        else if( xml->getAttributeValue("mapx1") )
                        {
                            p1 = Point( MapPoint, xml->getAttributeValueAsInt("mapx1"), xml->getAttributeValueAsInt("mapy1"), 0 );
                            p2 = Point( MapPoint, xml->getAttributeValueAsInt("mapx2"), xml->getAttributeValueAsInt("mapy2"), 0 );
                        }
                        else if( xml->getAttributeValue("tilex1") )
                        {
                            p1 = Point( TilePoint, xml->getAttributeValueAsInt("tilex1"), xml->getAttributeValueAsInt("tiley1"), 0 );
                            p2 = Point( TilePoint, xml->getAttributeValueAsInt("tilex2"), xml->getAttributeValueAsInt("tiley2"), 0 );
                        }
                        else
                        {
                            p1 = Point( TilePoint, 0, 0 );
                            p2 = Point( TilePoint,this->getWidth(), this->getHeight() );
                        }

                        if( xml->getAttributeValue("visible") )
                            visible = (bool) xml->getAttributeValueAsInt("visible");

                        Area *area = new Area( p1, p2, visible );

                        if( xml->getAttributeValue("script") )
                            area->setOnCollisionScript( xml->getAttributeValue("script") );
                        else
                        {
                            xml->read();
                            area->setOnCollisionCode( xml->getNodeData() );
                            xml->read();
                        }

                        layer->addArea( area );
                    }
                    if( !strcmp("if", xml->getNodeName() ) )
                    {
                        /* Use a python boolean to define the result. */
                        bool result = true;

                        /* Only evaluate the if tag if we are allowed to use scripts. */
                        if( scripts )
                        {
                            result = engine->evaluatePythonBoolean( xml->getAttributeValue("code"),
                                                                    xml->getAttributeValue("cond") );
                        }

                        /* If the result was false, we want to read on until
                         * we come across the corresponding </if>.
                         * If the result was true, we simply ignore this if
                         * node. */
                        if( !result )
                        {
                            /* Seek until the end of this if node. */
                            int endNodesToFind = 1;
                            while( endNodesToFind>0 && xml->read() && xml )
                            {
                                if( !strcmp("if", xml->getNodeName() ) )
                                    endNodesToFind += (xml->getNodeType()==EXN_ELEMENT?1:-1);
                            }
                        }

                    }
                    if( !strcmp("onload", xml->getNodeName() ) )
                    {
                        /* Only if we are allowed to execute scripts. */
                        if( scripts )
                        {
                            if( xml->getAttributeValue("script") )
                            {
                                engine->runPythonScript( xml->getAttributeValue("script") );
                            }
                            else
                            {
                                xml->read();
                                engine->runPythonCode( xml->getNodeData() );
                                xml->read();
                            }
                        }
                    }
                    if( !strcmp("onprerender", xml->getNodeName() ) )
                    {
                        if( xml->getAttributeValue("script") )
                        {
                            onPreRenderScript = new char[ strlen(xml->getAttributeValue("script"))+1 ];
                            strcpy( onPreRenderScript, xml->getAttributeValue("script") );
                        }
                        else
                        {
                            xml->read();
                            onPreRenderCode = new char[ strlen(xml->getNodeData())+1 ];
                            strcpy( onPreRenderCode, xml->getNodeData() );
                            xml->read();

                            engine->toPythonCode( &onPreRenderCode );
                        }
                    }
                    if( !strcmp("onpostrender", xml->getNodeName() ) )
                    {
                        if( xml->getAttributeValue("script") )
                        {
                            onPostRenderScript = new char[ strlen(xml->getAttributeValue("script"))+1 ];
                            strcpy( onPostRenderScript, xml->getAttributeValue("script") );
                        }
                        else
                        {
                            xml->read();
                            onPostRenderCode = new char[ strlen(xml->getNodeData())+1 ];
                            strcpy( onPostRenderCode, xml->getNodeData() );
                            xml->read();

                            engine->toPythonCode( &onPostRenderCode );
                        }
                    }
                    break;

                case EXN_ELEMENT_END:
                    if( !strcmp("layer", xml->getNodeName()) )
                    {
                        layers.push_back( layer );
                        layer = 0;
                    }
                    break;
            }
        }

        delete xml;

        /* Initial updates. */
        sortLayers();
        depthSort();
    }

    Map::Map( int w, int h, const char *tileSetFilename ): width(w), height(h), sortedLayers(0), currentLayer(0), onPreRenderCode(0), onPreRenderScript(0), onPostRenderCode(0), onPostRenderScript(0)
    {
        tileSet = new TileSet( tileSetFilename );
        Layer *layer =  new Layer( tileSet, width, height, 0xff, 0 );
        layer->setTiles( 0 );
        layers.push_back( layer );
        sortLayers();

        strcpy( fileName, "untitled" );
    }

    Map::~Map()
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            delete layers[i];
        delete tileSet;

        if( onPreRenderScript )
            delete[] onPreRenderScript;
        if( onPreRenderCode )
            delete[] onPreRenderCode;

        if( onPostRenderScript )
            delete[] onPostRenderScript;
        if( onPostRenderCode )
            delete[] onPostRenderCode;
    }

    Layer *Map::getCurrentLayer() const
    {
        return layers[currentLayer];
    }

    Layer *Map::getLayer( int n ) const
    {
        return layers[n];
    }

    int Map::getCurrentLayerIndex() const
    {
        return currentLayer;
    }

    void Map::setCurrentLayer( int index )
    {
        currentLayer = index;
    }

    int Map::getNumberOfLayers() const
    {
        return (int) layers.size();
    }

    const char *Map::getFileName() const
    {
        return fileName;
    }

    int Map::getWidth() const
    {
        return width;
    }

    int Map::getHeight() const
    {
        return height;
    }

    void Map::addNewLayer( int z )
    {
        Layer *layer =  new Layer( tileSet, width, height, 0xff, z );
        layer->setTiles( 0 );
        layers.push_back( layer );

        setCurrentLayer( (int)layers.size()-1 );

        sortLayers();
    }

    TileSet *Map::getTileSet() const
    {
        return tileSet;
    }

    StaticObject *Map::getObject( const char *name )
    {
        /* Look in the current layer first. */
        if( layers.size() )
        {
            StaticObject *so = layers[currentLayer]->getObject( name );
            if( so )
                return so;
        }

        /* Go through all other layers. */
        for( unsigned int i=0; i<layers.size(); i++ )
        {
            if( i!=currentLayer )
            {
                StaticObject *so = layers[i]->getObject( name );
                if( so )
                    return so;
            }
        }

        return 0;
    }

    Person *Map::getPerson( const char *name )
    {
        StaticObject *object = getObject( name );
        if( object->getEntityType() != PersonEntity )
            getLogManager()->warning( "Requested StaticObject '%s' as Person, but this is a StaticObject.", name );
        return (Person*) object;
    }

    void Map::addObject( StaticObject *so, Point position )
    {
        layers[currentLayer]->addObject( so, position );
    }

    void Map::removeObject( StaticObject *so )
    {
        for( unsigned int i=0; i<layers.size(); i++ )
        {
            layers[i]->removeObject( so );
        }
    }

    void Map::update()
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            layers[i]->update();
    }

    void Map::draw( bool scripts ) const
    {
        if( scripts )
            this->onPreRender();

        videoManager->push();

        for( unsigned int i=0; i<layers.size(); i++ )
            sortedLayers[i]->draw();

        videoManager->pop();

        if( scripts )
            this->onPostRender();
    }

    void Map::depthSort()
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            layers[i]->depthSort();
    }

    void Map::sortLayers()
    {
        if( sortedLayers )
            delete[] sortedLayers;

        sortedLayers = new Layer*[layers.size()+1];
        for( unsigned int i=0; i<layers.size(); i++ )
            sortedLayers[i] = layers[i];

        /* A insertion-sort. */
        for( unsigned int i=0; i+1<layers.size(); i++ )
        {
            for( unsigned int j=i+1; j<layers.size(); j++ )
            {
                if( sortedLayers[j]->getZ() < sortedLayers[i]->getZ() )
                {
                    Layer *temp = sortedLayers[j];
                    sortedLayers[j] = sortedLayers[i];
                    sortedLayers[i] = temp;
                }
            }
        }

        sortedLayers[ layers.size() ] = 0;
    }

    void Map::onPreRender() const
    {
        Engine *engine = getEngine();

        videoManager->push();
        videoManager->reset();
        if( onPreRenderScript )
            engine->runPythonScript( onPreRenderScript );
        if( onPreRenderCode )
            engine->runPythonCode( onPreRenderCode );
        videoManager->pop();
    }

    void Map::onPostRender() const
    {
        Engine *engine = getEngine();

        videoManager->push();
        videoManager->reset();
        if( onPostRenderScript )
            engine->runPythonScript( onPostRenderScript );
        if( onPostRenderCode )
            engine->runPythonCode( onPostRenderCode );
        videoManager->pop();
    }

};
