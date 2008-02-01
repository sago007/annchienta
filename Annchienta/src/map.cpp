/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "map.h"

#include <GL/gl.h>
#include "tile.h"
#include "tileset.h"
#include "auxfunc.h"
#include "entity.h"
#include "layer.h"

namespace Annchienta
{

    Map::Map( const char *filename ): currentLayer(0)
    {
        width = 20, height = 20;

        tileSet = new TileSet( filename );

        Tile **tiles = new Tile*[width*height];

        for( int y=0; y<height; y++ )
        {
            for( int x=0; x<width; x++ )
            {
                Point points[4];
                points[0].x = points[1].x = x;
                points[2].x = points[3].x = x+1;
                points[0].y = points[3].y = y;
                points[1].y = points[2].y = y+1;

                Surface *surfaces[4];

                for( int i=0; i<4; i++ )
                {
                    points[i].setType( TilePoint );
                    points[i].z = 0;//randInt(30);
                    surfaces[i] = tileSet->getSurface( 1+randInt(2) );
                }

                tiles[y*width+x] = new Tile( points[0], surfaces[0], points[1], surfaces[1], points[2], surfaces[2], points[3], surfaces[3] );
            }
        }

        layers.push_back( new Layer( width, height, tiles ) );

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
