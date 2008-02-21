/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "map.h"

#include <GL/gl.h>
#include <sstream>
#include <vector>
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

namespace Annchienta
{

    Map::Map( const char *filename ): currentLayer(0)
    {
        Tile **tiles = 0;
        Layer *layer = 0;
        Annchienta::LayerInfo *layerInfo;
        std::vector<Entity*> entities;

        IrrXMLReader *xml = createIrrXMLReader( filename );

        if( !xml )
            printf("Could not open level file %s\n", filename );

        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    if( !strcmpCaseInsensitive("map", xml->getNodeName()) )
                    {
                        width = xml->getAttributeValueAsInt("width");
                        height = xml->getAttributeValueAsInt("height");

                        tiles = new Tile*[width*height];

                        getMapManager()->setTileWidth( xml->getAttributeValueAsInt("tilewidth") );
                        getMapManager()->setTileHeight( xml->getAttributeValueAsInt("tileheight") );

                        tileSet = new TileSet( xml->getAttributeValue("tileset") );
                    }
                    if( !strcmpCaseInsensitive("layer", xml->getNodeName()) )
                    {
                        layerInfo = new LayerInfo;
                        layerInfo->z = xml->getAttributeValue("z") ? xml->getAttributeValueAsInt("z"):0;
                        layerInfo->width = width;
                        layerInfo->height = height;
                        layerInfo->opacity = xml->getAttributeValue("opacity") ? xml->getAttributeValueAsInt("opacity"):0xff;
                        tiles = 0;
                    }
                    if( !strcmpCaseInsensitive("tiles", xml->getNodeName()) )
                    {
                        xml->read();
                        std::stringstream data( xml->getNodeData() );

                        tiles = new Tile*[width*height];

                        for( int y=0; y<height; y++ )
                        {
                            for( int x=0; x<width; x++ )
                            {
                                Point points[4];
                                int surfaces[4];
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

                                data >> sideSurface;

                                tiles[y*width+x] = new Tile( points[0], tileSet->getSurface( surfaces[0] ),
                                                             points[1], tileSet->getSurface( surfaces[1] ),
                                                             points[2], tileSet->getSurface( surfaces[2] ),
                                                             points[3], tileSet->getSurface( surfaces[3] ),
                                                             tileSet->getSideSurface( sideSurface ) );

                            }
                        }
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

                        entities.push_back( staticObject );

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

                        entities.push_back( person );

                    }
                    break;

                case EXN_ELEMENT_END:
                    if( !strcmpCaseInsensitive("layer", xml->getNodeName()) )
                    {
                        Layer *layer = new Layer( layerInfo, tiles );
                        delete layerInfo;

                        for( unsigned int i=0; i<entities.size(); i++ )
                            layer->addEntity( entities[i] );

                        entities.clear();

                        layer->setTileSet( tileSet );

                        layers.push_back( layer );
                    }
                    break;
            }
        }

        delete xml;
    }

    Map::Map( int w, int h, const char *tileSetFilename )
    {
        tileSet = new TileSet( tileSetFilename );
        LayerInfo *layerInfo = new LayerInfo;
        layerInfo->z = 0;
        layerInfo->width = width = w;
        layerInfo->height = height = h;
        layerInfo->opacity = 0xff;
        Layer *layer =  new Layer( layerInfo, 0 );
        layer->setTileSet( tileSet );
        delete layerInfo;
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

    void Map::setCurrentLayer( int index )
    {
        currentLayer = index;
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

    void Map::update()
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            layers[i]->update();
    }

    void Map::draw() const
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            layers[i]->draw();
    }

    void Map::drawTerrain() const
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            layers[i]->drawTerrain();
    }

    void Map::depthSort()
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            layers[i]->depthSort();
    }

};
