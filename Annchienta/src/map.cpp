/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "map.h"

#include <GL/gl.h>
#include "tile.h"
#include "tileset.h"
#include "auxfunc.h"
#include "entity.h"

namespace Annchienta
{

    Map::Map( const char *filename )
    {
        width = 20;
        height = 20;

        tileSet = new TileSet( filename );

        tiles = new Tile*[width*height];

        /* Create some extra space.
         */
        entities.resize( width*height );

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
                    points[i].z = randInt( 5 );
                    if( x==4 && y==0 )
                        points[i].z = 16 + randInt(20);
                    surfaces[i] = tileSet->getSurface( randInt(2) );
                }

                entities[y*width+x] = tiles[y*width+x] = new Tile( points[0], surfaces[0], points[1], surfaces[1], points[2], surfaces[2], points[3], surfaces[3] );
            }
        }
    }

    Map::~Map()
    {
        delete tileSet;

        for( int i=0; i<width*height; i++ )
        {
            delete tiles[i];
        }
        delete[] tiles;
    }

    void Map::draw() const
    {

        glPushMatrix();

        for( unsigned int i=0; i<entities.size(); i++ )
            entities[i]->draw();

        glColor4f( 1.0f, 1.0f, 1.0f, 1.0f );

        glPopMatrix();
    }

    void Map::depthSort()
    {
        /* The map should be more or less sorted already, that's
         * why we use a form of gnome sort.
         */
        unsigned int i=1, c=1;
        while( i<entities.size() )
        {
            if( entities[i-1]->getDepthSortY() > entities[i]->getDepthSortY() )
            {
                swap<Entity*>( entities[i-1], entities[i] );
                if( i>1 )
                    i--;
            }
            else
            {
                i = i>=c?i+1:c;
                c = i;
            }
        }
    }

};
