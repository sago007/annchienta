/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "tile.h"

#include <GL/gl.h>
#include <stdio.h>
#include "surface.h"

namespace Annchienta
{

    void Tile::makeList()
    {

        /* Get the texture coordinates.
         */
        float xCoord = 0.5f*( surfaces[0]->getRightTexCoord() + surfaces[0]->getLeftTexCoord() );
        float yCoord = 0.5f*( surfaces[0]->getTopTexCoord() + surfaces[0]->getBottomTexCoord() );

        /* Set some more values.
         */
        int numberOfSurfaces = 0;
        Surface *orderedSurfaces[5] = { 0, 0, 0, 0, 0 };
        int surfaceCount[4] = { 1, 0, 0, 0 };

        /* Count how many surfaces there are of each, save to surfaceCount[].
         */
        for( int i=0; i<4; i++ )
        {
            for( int b=0; b>=0 && b<i; b++ )
            {
                if( surfaces[b] == surfaces[i] )
                {
                    surfaceCount[b]++;
                    b = i;
                }
                else
                {
                    if( b+1>=i )
                        surfaceCount[i]++;
                }
            }
        }

        /* Now get the total number of Surfaces.
         */
        for( int i=0; i<4; i++ )
            if( surfaceCount[i] )
                numberOfSurfaces++;

        /* Sort the surfaces.
         */
        for( int i=0, b=0; i<4; i++ )
        {
            if( surfaceCount[i] )
            {
                orderedSurfaces[b] = surfaces[i];
                b++;
            }
        }

        //printf( "Surface count: %d, %d, %d, %d.\n", surfaceCount[0], surfaceCount[1], surfaceCount[2], surfaceCount[3] );

        /* Create a new display list for this tile.
         */
        list = glGenLists( 1 );
        glNewList( list, GL_COMPILE );

        /* For every surface, draw with thee correct alpha value
         * at the correct points.
         */
        for( int i=0; i<numberOfSurfaces; i++ )
        {

            glBindTexture( GL_TEXTURE_2D, orderedSurfaces[i]->getTexture() );
            glBegin( GL_QUADS );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[0]?1.0f:0.0f );
                glTexCoord2f( xCoord, surfaces[0]->getTopTexCoord() );
                glVertex2f( points[0].x, points[0].y );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[1]?1.0f:0.0f );
                glTexCoord2f( surfaces[0]->getLeftTexCoord(), yCoord );
                glVertex2f( points[1].x, points[1].y );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[2]?1.0f:0.0f );
                glTexCoord2f( xCoord, surfaces[0]->getBottomTexCoord() );
                glVertex2f( points[2].x, points[2].y );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[3]?1.0f:0.0f );
                glTexCoord2f( surfaces[0]->getRightTexCoord(), yCoord );
                glVertex2f( points[3].x, points[3].y );

            glEnd();
        }

        /* End the display list.
         */
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
