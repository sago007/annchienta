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

#ifndef ANNCHIENTA_MASK_H
#define ANNCHIENTA_MASK_H

#include "Cacheable.h"

namespace Annchienta
{
    /** Masks are basically 2d arrays of boolean values used for
     *  pixel-perfect collision detection.
     */
    class Mask: public Cacheable
    {
        private:
            int width, height;
            bool *pixels;

        public:
            /** Creates a new mask from a valid PNG image.
             *  This image should be as large as the sprite it is
             *  used for. Collision pixels should be white (rgb(255,255,255))
             *  and ignore pixels should be black (rgb(0,0,0)).
             *  \param filename PNG image to load.
             */
            Mask( const char *filename );

            /** This creates a new mask with given dimensions. It will
             *  have the form of an isometric Tile by default, so you
             *  can directly use this to do tile collision.
             *  \param w Width for the new Mask.
             *  \param h Height for the new Mask.
             */
            Mask( int w, int h );
            ~Mask();

            virtual CacheableType getCacheableType() const;

            /** \return The width of this mask.
             */
            int getWidth() const;

            /** \return The height of this mask.
             */
            int getHeight() const;

            /** Check if this Mask collides with another Mask.
             *  \param x1 X coordinate of this Mask.
             *  \param y1 Y coordinate of this Mask.
             *  \param mask2 The other mask to check collision with.
             *  \param x2 X coordinate of the other Mask.
             *  \param y2 Y coordinate of the other Mask.
             *  \param box When set to true, do a quick bounding box collision check instead of a pixel-perfect collision check.
             *  \return If the two masks collide.
             */
            bool collision( int x1, int y1, Mask *mask2, int x2, int y2, bool box=false );

            /** Use this to edit a mask. Fills a rectangle with
             *  a certain value.
             *  \param x1 Top left x coordinate of the rectangle.
             *  \param y1 Top left y coordinate of the rectangle.
             *  \param x2 Bottom right x coordinate of the rectangle.
             *  \param y2 Bottom right y coordinate of the rectangle.
             *  \param value Value to fill the rectangle with. True for collision, false for transparency.
             */
            void fillRectangle( int x1, int y1, int x2, int y2, bool value );
    };
};

#endif
