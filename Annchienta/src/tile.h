/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_TILE_H
#define ANNCHIENTA_TILE_H

#include <GL/gl.h>
#include "point.h"
#include "entity.h"

namespace Annchienta
{

    class Surface;
    class TileSet;

    class Tile: public Entity
    {

        private:
            Point points[4];
            Point isoPoints[4];
            Surface *surfaces[4];
            Surface *sideSurface;
            GLuint list;

            TileSet *tileSet;
            int surfaceNumbers[4];
            int sideSurfaceNumber;
            int sideSurfaceOffset;

            bool nullTile;
            bool needsRecompiling;

            void makeList();

        public:
            Tile( TileSet*, Point, int, Point, int, Point, int, Point, int, int ssOffset=0, int ss=0 );
            ~Tile();

            virtual EntityType getEntityType() const;

            virtual void update();
            virtual void draw();
            virtual int getDepth();
            bool hasPoint( Point point );

            bool isNullTile() const;

            int setZ( int point, int z );
            int getZ( int point ) const;

            #ifndef SWIG
                virtual Point getMaskPosition() const;
                Point getPoint( int i ) const;
            #endif

            Point *getPointPointer( int i );
            void setSurface( int i, int s );
            void setSideSurface( int ss );
            void setSideSurfaceOffset( int sso );

            int getSurface( int i ) const;
            int getSideSurface() const;
            int getSideSurfaceOffset() const;

    };
};

#endif
