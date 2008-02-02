/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "map.h"

#include <GL/gl.h>
#include <sstream>
#include "xml/irrXML.h"
using namespace irr;
using namespace io;
#include "tile.h"
#include "tileset.h"
#include "auxfunc.h"
#include "entity.h"
#include "layer.h"
#include "mapmanager.h"

namespace Annchienta
{

    Map::Map( const char *filename ): currentLayer(0)
    {
        Tile **tiles = 0;
        Layer *layer = 0;

        IrrXMLReader *xml = createIrrXMLReader( filename );

        if( !xml )
            printf("Could not open level file %s\n", filename );

        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    if( !strcmp("map", xml->getNodeName()) )
                    {
                        width = xml->getAttributeValueAsInt("width");
                        height = xml->getAttributeValueAsInt("height");

                        tiles = new Tile*[width*height];

                        getMapManager()->setTileWidth( xml->getAttributeValueAsInt("tilewidth") );
                        getMapManager()->setTileHeight( xml->getAttributeValueAsInt("tileheight") );

                        tileSet = new TileSet( xml->getAttributeValue("tileset") );
                    }
                    if( !strcmp("layer", xml->getNodeName()) )
                    {
                        tiles = 0;
                    }
                    if( !strcmp("tiles", xml->getNodeName()) )
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

                                tiles[y*width+x] = new Tile( points[0], tileSet->getSurface( surfaces[0] ),
                                                             points[1], tileSet->getSurface( surfaces[1] ),
                                                             points[2], tileSet->getSurface( surfaces[2] ),
                                                             points[3], tileSet->getSurface( surfaces[3] ) );

                            }
                        }

                    }
                    break;

                case EXN_ELEMENT_END:
                    if( !strcmp("layer", xml->getNodeName()) )
                    {
                        layers.push_back( new Layer( width, height, tiles ) );
                    }
                    break;
            }
        }

        delete xml;
    }

    Map::Map( int w, int h, const char *tileSetFilename )
    {
        tileSet = new TileSet( tileSetFilename );
        layers.push_back( new Layer( w, h, 0 ) );
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

    void Map::draw() const
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            layers[i]->draw();
    }

    void Map::depthSort()
    {
        for( unsigned int i=0; i<layers.size(); i++ )
            layers[i]->depthSort();
    }

};
