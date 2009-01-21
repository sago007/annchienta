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
    class Mask;
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

            /* If the tile lies in the shadow or not.
             * Should be drawn darker in shadow, of
             * course...
             */
            bool shadowed;

            /* If the tile is a specially marked tile.
             * (this is usually when an area lies on it.)
             */
            bool visualIndication;

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
            virtual Mask *getMask() const;

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
                 *  \note Not available in Python.
                 */
                virtual Point getMaskPosition() const;

                /** Returns a point in this tile with the given index.
                 *  \note Not available in Python.
                 */
                Point getPoint( int i ) const;
            #endif

            /** Gets a reference to a Point of this Tile.
             *  You can use this when you actually want to
             *  change a Tile's properties (like when you're
             *  creating an editor). This function returns
             *  a MapPoint (\ref PointType).
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

            void setShadowed( bool shadowed );
            bool isShadowed() const;

            void setVisualIndication( bool visualIndication );
            bool hasVisualIndication() const;

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
