/*  This file is part of Annchienta.
 *  Copyright 2008 (C) Jasper Van der Jeugt
 *
 *  Annchienta is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Annchienta is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with Annchienta.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "Tile.h"

#include <GL/gl.h>
#include <cstdio>
#include "Surface.h"
#include "MapManager.h"
#include "TileSet.h"

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
        /* Should not happen, but might avoid segfaults.
         */
        if( nullTile )
            return;

        /* Obtain a reference to the map manager, because we
         * we need to know tile width and height.
         */
        MapManager *mapMgr = getMapManager();

        /* Set some more values.
         */
        int numberOfSurfaces = 0;
        Surface *orderedSurfaces[5] = { 0, 0, 0, 0, 0 };
        int surfaceCount[4] = { 1, 0, 0, 0 };

        /* Draw darker if this tile is shadowed.
         */
        float r=1.0, g=1.0, b=1.0;
        if( shadowed )
            r = g = b = 0.5;

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
        glNewList( list, GL_COMPILE_AND_EXECUTE );

        /* Don't draw back faces of tiles. */
        glEnable( GL_CULL_FACE );
        glPushMatrix();

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
    
                glColor4f( r, g, b, orderedSurfaces[i]==surfaces[0] || i==0?1.0f:0.0f );
                glTexCoord2f( xCenter, s->getTopTexCoord() );
                glVertex2f( (GLfloat)points[0].x, (GLfloat)(points[0].y-points[0].z) );
    
                glColor4f( r, g, b, orderedSurfaces[i]==surfaces[1] || i==0?1.0f:0.0f );
                glTexCoord2f( s->getLeftTexCoord(), yCenter );
                glVertex2f( (GLfloat)points[1].x, (GLfloat)(points[1].y-points[1].z) );
    
                glColor4f( r, g, b, orderedSurfaces[i]==surfaces[2] || i==0?1.0f:0.0f );
                glTexCoord2f( xCenter, s->getBottomTexCoord() );
                glVertex2f( (GLfloat)points[2].x, (GLfloat)(points[2].y-points[2].z) );
    
                glColor4f( r, g, b, orderedSurfaces[i]==surfaces[3] || i==0?1.0f:0.0f );
                glTexCoord2f( s->getRightTexCoord(), yCenter );
                glVertex2f( (GLfloat)points[3].x, (GLfloat)(points[3].y-points[3].z) );

            glEnd();
        }

        /* If there is a Z coordinate and a wall-like thing surface,
         * we want to draw a wall-like thing.
         */
        if( (points[1].z || points[2].z || points[3].z || sideSurfaceOffset) && sideSurface )
        {
            /* Get come specific texture coords.
             */
            float centerX = 0.5f*( sideSurface->getLeftTexCoord() + sideSurface->getRightTexCoord() );
            float topY = 1.0f -  ((float)(mapMgr->getTileHeight()/2))/(float)sideSurface->getGlHeight();
            float downY = 1.0f -  ((float)(sideSurface->getHeight()-mapMgr->getTileHeight()/2))/(float)sideSurface->getGlHeight();

            /* Use a triangle strip to draw a
             *     -       -
             *     ||-   -||
             *     -|||-|||-   - like thingy.
             *       -|||-
             *         -
             */
            glColor4f( r, g, b, 1.0f );
            glBindTexture( GL_TEXTURE_2D, sideSurface->getTexture() );
            //sideSurface->draw( points[1].x, points[0].y-points[0].z );
            glBegin( GL_TRIANGLE_STRIP );

                glTexCoord2f( sideSurface->getLeftTexCoord(), sideSurface->getTopTexCoord() );
                glVertex2f( (GLfloat)points[1].x, (GLfloat)(points[1].y - points[1].z) );

                glTexCoord2f( sideSurface->getLeftTexCoord(), downY );
                glVertex2f( (GLfloat)points[1].x, (GLfloat)(points[1].y - sideSurfaceOffset) );

                glTexCoord2f( centerX, topY );
                glVertex2f( (GLfloat)points[2].x, (GLfloat)(points[2].y - points[2].z) );

                glTexCoord2f( centerX, sideSurface->getBottomTexCoord() );
                glVertex2f( (GLfloat)points[2].x, (GLfloat)(points[2].y - sideSurfaceOffset) );

                glTexCoord2f( sideSurface->getRightTexCoord(), sideSurface->getTopTexCoord() );
                glVertex2f( (GLfloat)points[3].x, (GLfloat)(points[3].y - points[3].z) );

                glTexCoord2f( sideSurface->getRightTexCoord(), downY );
                glVertex2f( (GLfloat)points[3].x, (GLfloat)(points[3].y - sideSurfaceOffset) );

            glEnd();
        }

        glPopMatrix();
        
        /* Reset face culling. */
        glDisable( GL_CULL_FACE );
        
        /* End the display list.
         */
        glEndList();
    }


    Tile::Tile( TileSet *ts, Point p0, int s0, Point p1, int s1, Point p2, int s2,
                Point p3, int s3, int sso, int side ): Entity("tile"), list(0), tileSet(ts),
                sideSurfaceOffset(sso), shadowed(false), nullTile(false), needsRecompiling(true),
                obstruction(DefaultObstruction)
    {
        points[0] = p0;
        surfaceNumbers[0] = s0;
        points[1] = p1;
        surfaceNumbers[1] = s1;
        points[2] = p2;
        surfaceNumbers[2] = s2;
        points[3] = p3;
        surfaceNumbers[3] = s3;
        sideSurface = tileSet->getSideSurface(side);
        sideSurfaceNumber = side;

        for( int i=0; i<4; i++ )
        {
            surfaces[i] = tileSet->getSurface( surfaceNumbers[i] );

            isoPoints[i] = points[i];
            points[i].convert( MapPoint );
            isoPoints[i].convert( IsometricPoint );
        }

        if( !(surfaces[0] && surfaces[1] && surfaces[2] && surfaces[3]) )
            nullTile = true;
    }

    Tile::~Tile()
    {
        glDeleteLists( list, 1 );
    }

    EntityType Tile::getEntityType() const
    {
        return TileEntity;
    }

    void Tile::update()
    {
    }

    void Tile::draw()
    {
        /* Tile is already drawn...
         */
        if( this->isDrawn() )
            return;

        if( !nullTile )
        {
            if( needsRecompiling )
            {
                makeList();
                needsRecompiling = false;
            }
            else
                glCallList( list );
        }

        setDrawn( true );
    }

    int Tile::getDepth()
    {
        return points[2].y;
    }

    bool Tile::hasPoint( Point point )
    {
        point.convert( IsometricPoint );
        return point.isEnclosedBy( &isoPoints[0], &isoPoints[2] );
        //return( point.x >= isoPoints[0].x && point.x <= isoPoints[3].x && point.y >= isoPoints[0].y && point.y <= isoPoints[1].y );
    }

    bool Tile::isNullTile() const
    {
        return nullTile;
    }

    void Tile::setZ( int point, int z )
    {
        points[point].z = z;

        needsRecompiling = true;
    }

    int Tile::getZ( int point ) const
    {
        return points[point].z;
    }

    Point Tile::getMaskPosition() const
    {
        return Point( MapPoint, points[1].x, points[0].y );
    }

    Point Tile::getPoint( int i ) const
    {
        return points[i];
    }

    Point *Tile::getPointPointer( int i )
    {
        return &points[i];
    }

    void Tile::setSurface( int i, int s )
    {
        surfaceNumbers[i] = s;
        surfaces[i] = tileSet->getSurface(s);
        if( surfaces[0] && surfaces[1] && surfaces[2] && surfaces[3] )
            nullTile = false;
        else
            nullTile = true;

        needsRecompiling = true;
    }

    void Tile::setSideSurface( int side )
    {
        sideSurface = tileSet->getSideSurface(side);
        sideSurfaceNumber = side;

        needsRecompiling = true;
    }

    void Tile::setSideSurfaceOffset( int sso )
    {
        sideSurfaceOffset = sso;

        needsRecompiling = true;
    }

    int Tile::getSurface( int i ) const
    {
        return surfaceNumbers[i];
    }

    int Tile::getSideSurface() const
    {
        return sideSurfaceNumber;
    }

    int Tile::getSideSurfaceOffset() const
    {
        return sideSurfaceOffset;
    }

    void Tile::setShadowed( bool shadow )
    {
        shadowed = shadow;
        needsRecompiling = true;
    }

    bool Tile::isShadowed() const
    {
        return shadowed;
    }

    void Tile::setObstructionType( ObstructionType o )
    {
        obstruction = o;
    }

    ObstructionType Tile::getObstructionType() const
    {
        return obstruction;
    }

};
