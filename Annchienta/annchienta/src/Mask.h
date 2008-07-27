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
             */
            Mask( const char *filename );

            /** This creates a new mask with given dimensions. It will
             *  have the form of an isometric Tile by default.
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

            bool collision( int x1, int y1, Mask *mask2, int x2, int y2, bool box=false );

            void fillRectangle( int x1, int y1, int x2, int y2, bool value );
    };
};

#endif
