/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "map.h"

#include <GL/gl.h>
#include <sstream>
#include <vector>
#include <Python.h>
#include "xml/irrXML.h"
using namespace irr;
using namespace io;
#include "tile.h"
#include "tileset.h"
#include "auxfunc.h"
#include "entity.h"
#include "layer.h"
#include "mapmanager.h"
#include "staticobject.h"
#include "person.h"
#include "point.h"
#include "area.h"
#include "engine.h"

namespace Annchienta
{

    Map::Map( const char *_filename ): sortedLayers(0), currentLayer(0)
    {
        Layer *layer = 0;

        IrrXMLReader *xml = createIrrXMLReader( _filename );

        strcpy( filename, _filename );

        if( !xml )
            printf("Could not open level file %s\n", _filename );

        Engine *engine = getEngine();

        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    if( !strcmpCaseInsensitive("map", xml->getNodeName()) )
                    {
                        width = xml->getAttributeValueAsInt("width");
                        height = xml->getAttributeValueAsInt("height");

                        getMapManager()->setTileWidth( xml->getAttributeValueAsInt("tilewidth") );
                        getMapManager()->setTileHeight( xml->getAttributeValueAsInt("tileheight") );

                        tileSet = new TileSet( xml->getAttributeValue("tileset") );
                    }
                    if( !strcmpCaseInsensitive("layer", xml->getNodeName()) )
                    {
                        int opacity = xml->getAttributeValue("opacity") ? xml->getAttributeValueAsInt("opacity"):0xff,
                            z = xml->getAttributeValue("z") ? xml->getAttributeValueAsInt("z"):0;

                        layer = new Layer( tileSet, width, height, opacity, z );
                    }
                    if( !strcmpCaseInsensitive("tiles", xml->getNodeName()) )
                    {
                        xml->read();
                        std::stringstream data( xml->getNodeData() );

                        Tile **tiles = new Tile*[width*height];

                        for( int y=0; y<height; y++ )
                        {
                            for( int x=0; x<width; x++ )
                            {
                                Point points[4];
                                int surfaces[4];
                                int sideSurfaceOffset;
                                int sideSurface;

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
                    if( !strcmpCaseInsensitive("staticobject", xml->getNodeName() ) )
                    {
                        StaticObject *staticObject = new StaticObject( xml->getAttributeValue("name"),
                                                                       xml->getAttributeValue("config") );

                        if( xml->getAttributeValue("isox") && xml->getAttributeValue("isoy") )
                            staticObject->setPosition( Point( IsometricPoint, xml->getAttributeValueAsInt("isox"),
                                                       xml->getAttributeValueAsInt("isoy"), 0 ) );

                        if( xml->getAttributeValue("mapx") && xml->getAttributeValue("mapy") )
                            staticObject->setPosition( Point( MapPoint, xml->getAttributeValueAsInt("mapx"),
                                                       xml->getAttributeValueAsInt("mapy"), 0 ) );

                        if( xml->getAttributeValue("tilex") && xml->getAttributeValue("tiley") )
                            staticObject->setPosition( Point( TilePoint, xml->getAttributeValueAsInt("tilex"),
                                                       xml->getAttributeValueAsInt("tiley"), 0 ) );

                        if( xml->getAttributeValueAsInt("camera") )
                            getMapManager()->cameraFollow( staticObject );

                        layer->addEntity( staticObject );

                    }
                    if( !strcmpCaseInsensitive("person", xml->getNodeName() ) )
                    {
                        Person *person = new Person( xml->getAttributeValue("name"),
                                                     xml->getAttributeValue("config") );

                        if( xml->getAttributeValue("isox") && xml->getAttributeValue("isoy") )
                            person->setPosition( Point( IsometricPoint, xml->getAttributeValueAsInt("isox"),
                                                 xml->getAttributeValueAsInt("isoy"), 0 ) );

                        if( xml->getAttributeValue("mapx") && xml->getAttributeValue("mapy") )
                            person->setPosition( Point( MapPoint, xml->getAttributeValueAsInt("mapx"),
                                                 xml->getAttributeValueAsInt("mapy"), 0 ) );

                        if( xml->getAttributeValue("tilex") && xml->getAttributeValue("tiley") )
                            person->setPosition( Point( TilePoint, xml->getAttributeValueAsInt("tilex"),
                                                 xml->getAttributeValueAsInt("tiley"), 0 ) );

                        if( xml->getAttributeValueAsInt("camera") )
                            getMapManager()->cameraFollow( person);

                        layer->addEntity( person );

                    }
                    if( !strcmpCaseInsensitive("area", xml->getNodeName() ) )
                    {
                        Point p1, p2;

                        if( xml->getAttributeValue("isox1") )
                        {
                            p1 = Point( IsometricPoint, xml->getAttributeValueAsInt("isox1"), xml->getAttributeValueAsInt("isoy1"), 0 );
                            p2 = Point( IsometricPoint, xml->getAttributeValueAsInt("isox2"), xml->getAttributeValueAsInt("isoy2"), 0 );
                        }

                        if( xml->getAttributeValue("mapx1") )
                        {
                            p1 = Point( MapPoint, xml->getAttributeValueAsInt("mapx1"), xml->getAttributeValueAsInt("mapy1"), 0 );
                            p2 = Point( MapPoint, xml->getAttributeValueAsInt("mapx2"), xml->getAttributeValueAsInt("mapy2"), 0 );
                        }

                        if( xml->getAttributeValue("tilex1") )
                        {
                            p1 = Point( TilePoint, xml->getAttributeValueAsInt("tilex1"), xml->getAttributeValueAsInt("tiley1"), 0 );
                            p2 = Point( TilePoint, xml->getAttributeValueAsInt("tilex2"), xml->getAttributeValueAsInt("tiley2"), 0 );
                        }

                        Area *area = new Area( p1, p2 );

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
                    if( !strcmpCaseInsensitive("if", xml->getNodeName() ) )
                    {
                        bool result = engine->evaluatePythonBoolean( xml->getAttributeValue("code"),
                                                                     xml->getAttributeValue("cond") );
                        if( !result )
                        {
                            // go to the if ending node
                            int endNodesToFind = 1;
                            while( endNodesToFind>0 && xml->read() && xml )
                            {
                                if( !strcmp("if", xml->getNodeName() ) )
                                    endNodesToFind += (xml->getNodeType()==EXN_ELEMENT?1:-1);
                            }
                        }

                    }
                    if( !strcmpCaseInsensitive("onload", xml->getNodeName() ) )
                    {
                        if( xml->getAttributeValue("script") )
                        {
                            engine->runPythonScript( xml->getAttributeValue("script") );
                        }
                        else
                        {
                            xml->read();
                            PyRun_SimpleString( xml->getNodeData() );
                            xml->read();
                        }
                    }
                    break;

                case EXN_ELEMENT_END:
                    if( !strcmpCaseInsensitive("layer", xml->getNodeName()) )
                    {
                        layers.push_back( layer );
                        layer = 0;
                    }
                    break;
            }
        }

        delete xml;
        sortLayers();
    }

    Map::Map( int w, int h, const char *tileSetFilename ): width(w), height(h), sortedLayers(0), currentLayer(0)
    {
        tileSet = new TileSet( tileSetFilename );
        Layer *layer =  new Layer( tileSet, width, height, 0xff, 0 );
        layer->setTiles( 0 );
        layers.push_back( layer );
        sortLayers();

        strcpy( filename, "untitled" );
    }

    Map::~Map()
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            delete layers[i];
        delete tileSet;
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
        return filename;
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
        if( layers.size() )
        {
            StaticObject *so = layers[currentLayer]->getObject( name );
            if( so )
                return so;
        }
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

    void Map::addObject( StaticObject *so )
    {
        layers[currentLayer]->addEntity( so );
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

    void Map::draw() const
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            sortedLayers[i]->draw();
    }

    void Map::drawTerrain() const
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            sortedLayers[i]->drawTerrain();
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

        unsigned int i=0;
        for( int z=0; i<layers.size(); z++ )
        {
            for( unsigned int l=0; l<layers.size(); l++ )
            {
                if( layers[l]->getZ()==z )
                {
                    sortedLayers[i] = layers[l];
                    i++;
                }
            }
        }

        sortedLayers[ layers.size() ] = 0;
    }

};
