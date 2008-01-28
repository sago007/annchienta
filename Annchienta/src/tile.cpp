/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "tile.h"

#include <GL/gl.h>
#include "surface.h"

namespace Annchienta
{

    void Tile::makeList()
    {

        float xCoord = 0.5f*( surfaces[0]->getRightTexCoord() + surfaces[0]->getLeftTexCoord() );
        float yCoord = 0.5f*( surfaces[0]->getTopTexCoord() + surfaces[0]->getBottomTexCoord() );

        list = glGenLists( 1 );
        glNewList( list, GL_COMPILE );

        glBindTexture( GL_TEXTURE_2D, surfaces[0]->getTexture() );

        glBegin( GL_QUADS );

            glTexCoord2f( xCoord, surfaces[0]->getTopTexCoord() );
            glVertex2f( points[0].x, points[0].y );

            glTexCoord2f( surfaces[0]->getLeftTexCoord(), yCoord );
            glVertex2f( points[1].x, points[1].y );

            glTexCoord2f( xCoord, surfaces[0]->getBottomTexCoord() );
            glVertex2f( points[2].x, points[2].y );

            glTexCoord2f( surfaces[0]->getRightTexCoord(), yCoord );
            glVertex2f( points[3].x, points[3].y );

        glEnd();

        /* Optimised method.
         */
        //surfaces[0]->draw( points[1].x, points[0].y );

        glEndList();
    }

    Tile::Tile( Point p1, Surface *s1, Point p2, Surface *s2, Point p3, Surface *s3, Point p4, Surface *s4 ): list(0)
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

        makeList();
    }

    Tile::~Tile()
    {
    }

    void Tile::callList()
    {
        glCallList( list );
    }

};
