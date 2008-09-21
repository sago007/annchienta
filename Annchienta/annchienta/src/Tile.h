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

            /** Checks if the given point lies within this Tile.
             */
            bool hasPoint( Point point );

            /** A NullTile is a Tile that will not be drawn at all
             *  because it is entirely transparent. A Person will
             *  not be able to walk over this Tile either. A tile
             *  marked as a NullTile when one or more of it's points
             *  have a null surface.
             */
            bool isNullTile() const;

            /** Sets the Z value of a point.
             *  \param point Index of the point you want to set the Z for.
             *  \param z The new Z coordinate for this Point.
             */
            void setZ( int point, int z );

            /** Returns the Z coordinate of the Point with the
             *  index given by point.
             */
            int getZ( int point ) const;

            #ifndef SWIG
                /** Where the tile mask should be placed... this is
                 *  mostly used internally.
                 */
                virtual Point getMaskPosition() const;

                /** Returns a point in this tile with the given index.
                 */
                Point getPoint( int i ) const;
            #endif

            /** Gets a reference to a Point of this Tile.
             *  You can use this when you actually want to
             *  change a Tile's properties (like when you're
             *  creating an editor).
             */
            Point *getPointPointer( int i );

            /** Sets the top Surface of this Tile. When you want
             *  to construct a Tile from only one Surface, call
             *  this for all four indexes.
             *
             *  The s stands for the number of the Surface, as
             *  defined by the TileSet being used in this Map.
             */
            void setSurface( int index, int s );
            void setSideSurface( int ss );
            void setSideSurfaceOffset( int sso );

            int getSurface( int i ) const;
            int getSideSurface() const;
            int getSideSurfaceOffset() const;

            /** \brief Sets the ObstructionType.
             *
             *  There are three possibilities:
             *
             *  \li DefaultObstruction
             *
             *  The default value. Persons will be able to step on this Tile,
             *  depending on the height and the values set by
             *  MapManager.setMaxAscentHeight() and
             *  MapManager.setMaxDescentHeight().
             *
             *  \li NoObstruction
             *
             *  All Persons will always be able to step on this Tile,
             *  regardless of it's height.
             *
             *  \li FullObstruction
             *
             *  Nobody will ever be able to step on this Tile,
             *  regardless of it's height.
             *
             *  \param obstructionType The new ObstructionType for this tile.
             */
            void setObstructionType( ObstructionType obstructionType );
            ObstructionType getObstructionType() const;

    };
};

#endif
