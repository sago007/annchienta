/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "map.h"

#include <GL/gl.h>
#include "tile.h"
#include "math.h"

#define MAP_S 20

namespace Annchienta
{

    Map::Map( const char *filename )
    {
        tiles = new Tile*[MAP_S*MAP_S];
        for( int y=0; y<MAP_S; y++ )
        {
            for( int x=0; x<MAP_S; x++ )
            {
                Point points[4];
                points[0].x = points[1].x = x;
                points[2].x = points[3].x = x+1;
                points[0].y = points[3].y = y;
                points[1].y = points[2].y = y+1;

                for( int i=0; i<4; i++ )
                    points[i].z = 0;//randInt( 20 );

                tiles[y*MAP_S+x] = new Tile( points[0], 0, points[1], 0, points[2], 0, points[3], 0 );
            }
        }
    }

    Map::~Map()
    {
        for( int i=0; i<MAP_S*MAP_S; i++ )
        {
            delete tiles[i];
        }
        delete[] tiles;
    }

    void Map::draw()
    {

        glPushMatrix();

        glDisable( GL_TEXTURE_2D );
        glBegin( GL_QUADS );

        for( int y=0; y<MAP_S; y++ )
        {
            for( int x=0; x<MAP_S; x++ )
            {
                glColor3ub( randInt(255), randInt(255), randInt(255) );
                tiles[y*MAP_S+x]->draw();
            }
        }

        glEnd();
        glEnable( GL_TEXTURE_2D );

        glPopMatrix();
    }

};
