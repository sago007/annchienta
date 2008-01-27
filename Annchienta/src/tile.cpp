/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "tile.h"

#include <GL/gl.h>

namespace Annchienta
{

    Tile::Tile( Point p1, Surface *s1, Point p2, Surface *s2, Point p3, Surface *s3, Point p4, Surface *s4 )
    {
        points[0] = p1;
        surfaces[0] = s1;
        points[1] = p2;
        surfaces[1] = s2;
        points[2] = p3;
        surfaces[2] = s3;
        points[3] = p4;
        surfaces[3] = s4;

        for( int i=0; i<4; i++ )
        {
            points[i].setType( TilePoint );
            points[i].to( MapPoint );
        }
    }

    Tile::~Tile()
    {
    }

    void Tile::draw()
    {
        for( int i=0; i<4; i++ )
            glVertex2f( points[i].x, points[i].y );
    }

};
