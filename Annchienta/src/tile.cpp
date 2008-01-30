/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "tile.h"

#include <GL/gl.h>
#include <stdio.h>
#include "surface.h"
#include "mapmanager.h"

namespace Annchienta
{

    void Tile::getTexCoords( Surface *surf, float *xCenter, float *topYCenter, float *topYDown, float *wallYDown ) const
    {
        MapManager *mapMgr = getMapManager();
        *xCenter = 0.5f*( surf->getLeftTexCoord() + surf->getRightTexCoord() );
        *topYCenter = 1.0f - (float)(mapMgr->getTileHeight()>>1)/(float)surf->getGlHeight();
        *topYDown = 1.0f - (float)(mapMgr->getTileHeight())/(float)surf->getGlHeight();
        *wallYDown = 1.0f - (float)( (mapMgr->getTileHeight()>>1) + surf->getHeight() - mapMgr->getTileHeight() )/(float)surf->getGlHeight();
    }

    void Tile::makeList()
    {
        /* Obtain a reference to the map manager, because we
         * we need to know tile width and height.
         */
        MapManager *mapMgr = getMapManager();

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

        /* Create a new display list for this tile.
         */
        list = glGenLists( 1 );
        glNewList( list, GL_COMPILE );

        float xCenter, topYCenter, topYDown, wallYDown;

        /* For every surface, draw with thee correct alpha value
         * at the correct points.
         */
        for( int i=0; i<numberOfSurfaces; i++ )
        {

            Surface *s = orderedSurfaces[i];

            /* Get texture coordinates.
             */
            this->getTexCoords( s, &xCenter, &topYCenter, &topYDown, &wallYDown );

            glBindTexture( GL_TEXTURE_2D, orderedSurfaces[i]->getTexture() );
            glBegin( GL_QUADS );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[0] || i==0?1.0f:0.0f );
                glTexCoord2f( xCenter, s->getTopTexCoord() );
                glVertex2f( points[0].x, points[0].y );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[1] || i==0?1.0f:0.0f );
                glTexCoord2f( s->getLeftTexCoord(), topYCenter );
                glVertex2f( points[1].x, points[1].y );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[2] || i==0?1.0f:0.0f );
                glTexCoord2f( xCenter, topYDown );
                glVertex2f( points[2].x, points[2].y );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[3] || i==0?1.0f:0.0f );
                glTexCoord2f( s->getRightTexCoord(), topYCenter );
                glVertex2f( points[3].x, points[3].y );

            glEnd();
        }

        /* If there is a Z coordinate, we want to draw a wall-like thing.
         */
        if( points[1].z || points[2].z || points[3].z )
        {
            Surface *s = surfaces[2];

            /* Get texture coords.
             */
            this->getTexCoords( s, &xCenter, &topYCenter, &topYDown, &wallYDown );

            /* Take the texture of point 2 and draw the wall to both sides.
             */
            glBindTexture( GL_TEXTURE_2D, s->getTexture() );
            glColor4f( 1.0f, 1.0f, 1.0f, 1.0f );
            glBegin( GL_TRIANGLE_STRIP );

                glTexCoord2f(s->getLeftTexCoord(), topYCenter );
                glVertex2f( points[1].x, points[1].y );

                glTexCoord2f( s->getLeftTexCoord(), wallYDown );
                glVertex2f( points[1].x, points[1].y + points[1].z );

                glTexCoord2f( xCenter, topYDown );
                glVertex2f( points[2].x, points[2].y );

                glTexCoord2f( xCenter, s->getBottomTexCoord() );
                glVertex2f( points[2].x, points[2].y + points[2].z );

                glTexCoord2f(s->getRightTexCoord(), topYCenter );
                glVertex2f( points[3].x, points[3].y );

                glTexCoord2f( s->getRightTexCoord(), wallYDown );
                glVertex2f( points[3].x, points[3].y + points[3].z );

            glEnd();

            /* Now the left wall, if needed.
             */
            if( surfaces[1] != surfaces[2] )
            {
                s = surfaces[1];
                this->getTexCoords( s, &xCenter, &topYCenter, &topYDown, &wallYDown );

                glBindTexture( GL_TEXTURE_2D, s->getTexture() );
                glBegin( GL_QUADS );

                    glColor4f( 1.0f, 1.0f, 1.0f, 1.0f );
                    glTexCoord2f(s->getLeftTexCoord(), topYCenter );
                    glVertex2f( points[1].x, points[1].y );
    
                    glTexCoord2f( s->getLeftTexCoord(), wallYDown );
                    glVertex2f( points[1].x, points[1].y + points[1].z );
    
                    glColor4f( 1.0f, 1.0f, 1.0f, 0.0f );
                    glTexCoord2f( xCenter, s->getBottomTexCoord() );
                    glVertex2f( points[2].x, points[2].y + points[2].z );

                    glTexCoord2f( xCenter, topYDown );
                    glVertex2f( points[2].x, points[2].y );
    
                glEnd();
            }

            /* Now the right wall, if needed.
             */
            if( surfaces[3] != surfaces[2] )
            {
                s = surfaces[3];
                this->getTexCoords( s, &xCenter, &topYCenter, &topYDown, &wallYDown );

                glBindTexture( GL_TEXTURE_2D, s->getTexture() );
                glBegin( GL_QUADS );

                    glColor4f( 1.0f, 1.0f, 1.0f, 0.0f );
                    glTexCoord2f( xCenter, topYDown );
                    glVertex2f( points[2].x, points[2].y );
    
                    glTexCoord2f( xCenter, s->getBottomTexCoord() );
                    glVertex2f( points[2].x, points[2].y + points[2].z );
    
                    glColor4f( 1.0f, 1.0f, 1.0f, 1.0f );
                    glTexCoord2f( s->getRightTexCoord(), wallYDown );
                    glVertex2f( points[3].x, points[3].y + points[3].z );

                    glTexCoord2f(s->getRightTexCoord(), topYCenter );
                    glVertex2f( points[3].x, points[3].y );
    
                glEnd();
            }

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

        if( surfaces[0] )
            makeList();
    }

    Tile::~Tile()
    {
    }

    void Tile::draw() const
    {
        if( surfaces[0] )
            glCallList( list );
    }

    int Tile::getDepthSortY() const
    {
        return points[2].y;
    }

};
