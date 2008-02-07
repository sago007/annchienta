/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MASK_H
#define ANNCHIENTA_MASK_H

namespace Annchienta
{
    class Mask
    {
        private:
            int width, height;
            bool *pixels;

        public:
            Mask( const char *filename );
            ~Mask();

            int getWidth() const;
            int getHeight() const;

            bool collision( int x1, int y1, Mask *mask2, int x2, int y2 );
    };
};

#endif
