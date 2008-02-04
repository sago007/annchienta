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

    /*void Tile::getTexCoords( Surface *surf, float *xCenter, float *topYCenter, float *topYDown, float *wallYDown ) const
    {
        MapManager *mapMgr = getMapManager();
        *xCenter = 0.5f*( surf->getLeftTexCoord() + surf->getRightTexCoord() );
        *topYCenter = 1.0f - (float)(mapMgr->getTileHeight()>>1)/(float)surf->getGlHeight();
        *topYDown = 1.0f - (float)(mapMgr->getTileHeight())/(float)surf->getGlHeight();
        *wallYDown = 1.0f - (float)( (mapMgr->getTileHeight()>>1) + surf->getHeight() - mapMgr->getTileHeight() )/(float)surf->getGlHeight();
    }*/

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
        if( !list )
            list = glGenLists( 1 );
        glNewList( list, GL_COMPILE );

        /* For every surface, draw with thee correct alpha value
         * at the correct points.
         */
        for( int i=0; i<numberOfSurfaces; i++ )
        {

            Surface *s = orderedSurfaces[i];

            /* Get specific texture coordinates.
             */
            float xCenter = 0.5f*( s->getLeftTexCoord() + s->getRightTexCoord() );
            float yCenter = 0.5f*( s->getTopTexCoord() + s->getBottomTexCoord() );

            /* Draw the top surface.
             */
            glBindTexture( GL_TEXTURE_2D, orderedSurfaces[i]->getTexture() );
            glBegin( GL_QUADS );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[0] || i==0?1.0f:0.0f );
                glTexCoord2f( xCenter, s->getTopTexCoord() );
                glVertex2f( points[0].x, points[0].y );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[1] || i==0?1.0f:0.0f );
                glTexCoord2f( s->getLeftTexCoord(), yCenter );
                glVertex2f( points[1].x, points[1].y );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[2] || i==0?1.0f:0.0f );
                glTexCoord2f( xCenter, s->getBottomTexCoord() );
                glVertex2f( points[2].x, points[2].y );
    
                glColor4f( 1.0f, 1.0f, 1.0f, orderedSurfaces[i]==surfaces[3] || i==0?1.0f:0.0f );
                glTexCoord2f( s->getRightTexCoord(), yCenter );
                glVertex2f( points[3].x, points[3].y );

            glEnd();
        }

        /* If there is a Z coordinate and a wall-like thing surface,
         * we want to draw a wall-like thing.
         */
        if( (points[1].z || points[2].z || points[3].z) && sideSurface )
        {
            /* Get come specific texture coords.
             */
            float centerX = 0.5f*( sideSurface->getLeftTexCoord() + sideSurface->getRightTexCoord() );
            float centerY = 1.0f -  (float)(sideSurface->getHeight()+1-mapMgr->getTileHeight()/2)/(float)sideSurface->getGlHeight();
            float centerYMinusOne = 1.0f -  (float)(sideSurface->getHeight()-mapMgr->getTileHeight()/2)/(float)sideSurface->getGlHeight();

            /* Use a triangle strip to draw a
             *     -       -
             *     ||-   -||
             *     -|||-|||-   - like thingy.
             *       -|||-
             *         -
             */
            glColor4f( 1.0f, 1.0f, 1.0f, 1.0f );
            glBindTexture( GL_TEXTURE_2D, sideSurface->getTexture() );
            glBegin( GL_TRIANGLE_STRIP );

                glTexCoord2f( sideSurface->getLeftTexCoord(), sideSurface->getTopTexCoord() );
                glVertex2f( points[1].x, points[1].y );

                glTexCoord2f( sideSurface->getLeftTexCoord(), centerYMinusOne );
                glVertex2f( points[1].x, points[1].y + points[1].z );

                glTexCoord2f( centerX, centerY );
                glVertex2f( points[2].x, points[2].y );

                glTexCoord2f( centerX, sideSurface->getBottomTexCoord() );
                glVertex2f( points[2].x, points[2].y + points[2].z );

                glTexCoord2f( sideSurface->getRightTexCoord(), sideSurface->getTopTexCoord() );
                glVertex2f( points[3].x, points[3].y );

                glTexCoord2f( sideSurface->getRightTexCoord(), centerYMinusOne );
                glVertex2f( points[3].x, points[3].y + points[3].z );

            glEnd();
        }

        /* End the display list.
         */
        glEndList();
    }

    Tile::Tile( Point p1, Surface *s1, Point p2, Surface *s2, Point p3, Surface *s3, Point p4, Surface *s4, Surface *side ): list(0), nullTile(false)
    {
        points[0] = p1;
        surfaces[0] = s1;
        points[1] = p2;
        surfaces[1] = s2;
        points[2] = p3;
        surfaces[2] = s3;
        points[3] = p4;
        surfaces[3] = s4;
        sideSurface = side;

        for( int i=0; i<4; i++ )
        {
            isoPoints[i] = points[i];
            points[i].to( MapPoint );
            isoPoints[i].to( IsometricPoint );
        }

        if( surfaces[0] && surfaces[1] && surfaces[2] && surfaces[3] )
            makeList();
        else
            nullTile = true;
    }

    Tile::~Tile()
    {
        glDeleteLists( list, 1 );
    }

    void Tile::draw()
    {
        /* Tile is already drawn...
         */
        if( drawn )
            return;

        if( !nullTile )
            glCallList( list );

        setDrawn( true );
    }

    int Tile::getDepthSortY() const
    {
        return points[2].y+points[2].z;
    }

};
