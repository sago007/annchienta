/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MASK_H
#define ANNCHIENTA_MASK_H

namespace Annchienta
{
    /** Masks are basically 2d arrays of boolean values used for
     *  pixel-perfect collision detection.
     */
    class Mask
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
             */
            void fillRectangle( int x1, int y1, int x2, int y2, bool value );
    };
};

#endif
