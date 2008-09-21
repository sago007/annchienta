/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_TILE_H
#define ANNCHIENTA_TILE_H

#include <SDL_opengl.h>
#include "Point.h"
#include "Entity.h"

namespace Annchienta
{

    enum ObstructionType
    {
        DefaultObstruction=0,
        NoObstruction=1,
        FullObstruction=2
    };

    class Surface;
    class TileSet;

/** \brief Holds a Tile.
 *
 * This class is used to hold parts of the Layer, called tiles.
 * Because we are using an isometric system, tiles are usually
 * shaped like a rhombus.
 *
 * A Tile consist of four Points, indexed like this:
 * \image html tile_pointindexes.png
 *
 * A Tile has a top Surface and a Side Surface.
 * \image html tile_anatomy.png
 */
class Tile(Entity):

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

            ObstructionType obstruction;

        public:
            Tile( TileSet*, Point, int, Point, int, Point, int, Point, int, int ssOffset=0, int ss=0 );
            ~Tile();

            virtual EntityType getEntityType() const;

            virtual void update();
            virtual void draw();
            virtual int getDepth();
            bool hasPoint( Point point );

            bool isNullTile() const;

            void setZ( int point, int z );
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

            void setObstructionType( ObstructionType o );
            ObstructionType getObstructionType() const;

    };
};

#endif
